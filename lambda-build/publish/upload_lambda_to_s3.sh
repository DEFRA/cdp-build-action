#!/bin/bash
set -euo pipefail

aws s3 cp output/"${FUNCTION_NAME}".zip s3://"${S3_BUCKET}/${FUNCTION_NAME}".zip
aws s3 cp --content-type text/plain output/"${FUNCTION_NAME}".zip.base64sha256 s3://"${S3_BUCKET}"/"${FUNCTION_NAME}".zip.base64sha256
