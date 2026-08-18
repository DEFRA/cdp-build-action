"""
Request a scoped GitHub App installation token from mono-lambda via API GW.

Called by the get-github-token-v2 composite action.
AWS credentials are read from environment variables already
set by configure-aws-credentials.

Environment variables (injected by action.yml):
  TOKEN_SERVICE_URL   Full URL of the /github/token endpoint
  AWS_REGION_NAME     AWS region for SigV4 signing (default: eu-west-2)

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

    now = datetime.datetime.utcnow()
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


# Main 

url = os.environ["TOKEN_SERVICE_URL"]
region = os.environ.get("AWS_REGION_NAME", "eu-west-2")
access_key = os.environ["AWS_ACCESS_KEY_ID"]
secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
session_token = os.environ.get("AWS_SESSION_TOKEN", "")

body = "{}"
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
    print(f"::error::Token service returned HTTP {exc.code}: {exc.read().decode()}", file=sys.stderr)
    sys.exit(1)

# The mono-lambda wraps its response as {"statusCode": 200, "body": {...}}
response_body = raw.get("body", raw)
if isinstance(response_body, str):
    response_body = json.loads(response_body)

if "token" not in response_body:
    print(f"::error::Unexpected response from token service: {raw}", file=sys.stderr)
    sys.exit(1)

token = response_body["token"]
repo = response_body.get("repository", "unknown")
expires_at = response_body.get("expires_at", "unknown")

print(f"::notice::Scoped token issued for {repo}, expires {expires_at}")

print(f"::add-mask::{token}")
with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
    fh.write(f"token={token}\n")
