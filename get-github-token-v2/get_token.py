"""
Request a scoped GitHub App installation token from the CDP token service.

Environment variables (injected by action.yml):
  TOKEN_SERVICE_URL   Full URL of the /github/token endpoint
  AWS_REGION_NAME     AWS region for SigV4 signing (default: eu-west-2)
  REPOSITORIES        Comma-separated repo short names, e.g. "cdp-opensearch-svc"
                      or "cdp-tf-svc-infra,cdp-tf-waf" for orchestrators

GitHub Actions OIDC variables (available in runner only when id-token: write is granted):
  ACTIONS_ID_TOKEN_REQUEST_URL    One-time endpoint to request the OIDC JWT
  ACTIONS_ID_TOKEN_REQUEST_TOKEN  Bearer token to authenticate the OIDC request

AWS credential env vars (set by configure-aws-credentials):
  AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY
  AWS_SESSION_TOKEN   (optional, present for assumed roles)
"""

import datetime
import hashlib
import hmac
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def _get_github_oidc_token(audience: str) -> str | None:
    """
    Fetch a GitHub OIDC JWT for the current workflow run.

    This proves to the lambda which repository is making the request.
    Only works when the calling workflow has granted ``id-token: write``
    permission.

    Args:
        audience: The ``aud`` claim to embed in the JWT.
                  We use ``https://github.com/DEFRA`` so the lambda can
                  verify it was issued specifically for the CDP token service.

    Returns:
        A signed JWT string, or None if OIDC is not available.
    """
    request_url = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_URL")
    request_token = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_TOKEN")

    if not request_url or not request_token:
        print(
            "::notice::oidc_token not sent — ACTIONS_ID_TOKEN_REQUEST_URL not available. "
            "Add 'permissions: id-token: write' to this workflow to enable "
            "repo-scoped enforcement.",
            file=sys.stderr,
        )
        return None

    url = f"{request_url}&audience={urllib.parse.quote(audience, safe='')}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {request_token}"},
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())["value"]
    except Exception as exc:  # noqa: BLE001
        # OIDC fetch failure must never break token issuance during migration.
        # The lambda will log the missing token and either warn (dry-run) or
        # block (enforcement mode), the action itself stays green.
        print(
            f"::warning::Failed to fetch GitHub OIDC token: {exc}. "
            "The request will proceed without it.",
            file=sys.stderr,
        )
        return None


def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _signing_key(secret_key: str, date_stamp: str, region: str, service: str) -> bytes:
    k = _sign(("AWS4" + secret_key).encode("utf-8"), date_stamp)
    k = _sign(k, region)
    k = _sign(k, service)
    k = _sign(k, "aws4_request")
    return k


def _sigv4_headers(
    method: str,
    url: str,
    body: str,
    region: str,
    service: str,
    access_key: str,
    secret_key: str,
    session_token: str,
) -> dict:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc
    path = parsed.path or "/"

    now = datetime.datetime.now(datetime.timezone.utc)
    amzdate = now.strftime("%Y%m%dT%H%M%SZ")
    datestamp = now.strftime("%Y%m%d")

    payload_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()

    headers_to_sign = {
        "content-type": "application/json",
        "host": host,
        "x-amz-date": amzdate,
    }
    if session_token:
        headers_to_sign["x-amz-security-token"] = session_token

    signed_headers = ";".join(sorted(headers_to_sign))
    canonical_headers = "".join(
        f"{k}:{headers_to_sign[k]}\n" for k in sorted(headers_to_sign)
    )

    canonical_request = "\n".join([
        method, path, "",
        canonical_headers, signed_headers, payload_hash,
    ])

    credential_scope = f"{datestamp}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join([
        "AWS4-HMAC-SHA256",
        amzdate,
        credential_scope,
        hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
    ])

    sig = hmac.new(
        _signing_key(secret_key, datestamp, region, service),
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    auth = (
        f"AWS4-HMAC-SHA256 Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={sig}"
    )

    result = {
        "Authorization": auth,
        "Content-Type": "application/json",
        "x-amz-date": amzdate,
        "Host": host,
    }
    if session_token:
        result["x-amz-security-token"] = session_token
    return result


# main
url = os.environ["TOKEN_SERVICE_URL"]
region = os.environ.get("AWS_REGION_NAME", "eu-west-2")
access_key = os.environ["AWS_ACCESS_KEY_ID"]
secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
session_token = os.environ.get("AWS_SESSION_TOKEN", "")

# Parse the comma-separated repositories list
repositories = [r.strip() for r in os.environ["REPOSITORIES"].split(",") if r.strip()]
if not repositories:
    print("::error::REPOSITORIES env var is empty — cannot determine which repos to scope the token to", file=sys.stderr)
    sys.exit(1)

# Fetch the GitHub OIDC token to prove which repo this workflow is running in
oidc_token = _get_github_oidc_token("https://github.com/DEFRA")

body_dict = {"repositories": repositories}
if oidc_token is not None:
    body_dict["oidc_token"] = oidc_token

body = json.dumps(body_dict)
headers = _sigv4_headers("POST", url, body, region, "execute-api", access_key, secret_key, session_token)

http_request = urllib.request.Request(
    url=url,
    data=body.encode("utf-8"),
    headers=headers,
    method="POST",
)

try:
    with urllib.request.urlopen(http_request) as resp:
        raw = json.loads(resp.read())
except urllib.error.HTTPError as exc:
    body_text = exc.read().decode(errors="replace")
    try:
        # Surface the Lambda error detail if the body is JSON
        detail = json.loads(body_text).get("body", body_text)
    except (json.JSONDecodeError, AttributeError):
        detail = body_text
    print(f"::error::Token service returned HTTP {exc.code}: {detail}", file=sys.stderr)
    sys.exit(1)

# The mono-lambda wraps its response as {"statusCode": 200, "body": {...}}
response_body = raw.get("body", raw)
if isinstance(response_body, str):
    response_body = json.loads(response_body)

if "token" not in response_body:
    print(f"::error::Unexpected response from token service: {raw}", file=sys.stderr)
    sys.exit(1)

token = response_body["token"]
repos = response_body.get("repositories", repositories)
expires_at = response_body.get("expires_at", "unknown")

print(f"::notice::Scoped token issued for {repos}, expires {expires_at}")

print(f"::add-mask::{token}")
with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
    fh.write(f"token={token}\n")
