"""
Request a scoped GitHub App installation token from the CDP token service.

Called by the get-github-token-v2 composite action.  AWS credentials are
already in the environment (set by configure-aws-credentials), so this script
just signs the request and parses the response.

Environment variables (set by action.yml):
  TOKEN_SERVICE_URL   Full URL of the /github/token endpoint
  AWS_REGION_NAME     AWS region for SigV4 signing (default: eu-west-2)
"""

import json
import os
import sys
import urllib.error
import urllib.request

import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

url = os.environ["TOKEN_SERVICE_URL"]
region = os.environ.get("AWS_REGION_NAME", "eu-west-2")

session = boto3.Session()
credentials = session.get_credentials()

request = AWSRequest(
    method="POST",
    url=url,
    data="{}",
    headers={"Content-Type": "application/json"},
)
SigV4Auth(credentials, "execute-api", region).add_auth(request)

http_request = urllib.request.Request(
    url=url,
    data=b"{}",
    headers=dict(request.headers),
    method="POST",
)

try:
    with urllib.request.urlopen(http_request) as resp:
        raw = json.loads(resp.read())
except urllib.error.HTTPError as exc:
    print(f"::error::Token service returned HTTP {exc.code}: {exc.read().decode()}", file=sys.stderr)
    sys.exit(1)

# The mono-lambda wraps its response as {"statusCode": 200, "body": {...}}
body = raw.get("body", raw)
if isinstance(body, str):
    body = json.loads(body)

if "token" not in body:
    print(f"::error::Unexpected response from token service: {raw}", file=sys.stderr)
    sys.exit(1)

token = body["token"]
repo = body.get("repository", "unknown")
expires_at = body.get("expires_at", "unknown")

print(f"::notice::Scoped token issued for {repo}, expires {expires_at}")

# Mask the token before writing to outputs
print(f"::add-mask::{token}")
with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
    fh.write(f"token={token}\n")
