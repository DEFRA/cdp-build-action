#!/bin/bash

if [[ -z "${FUNCTION_NAME}" ]]; then
  export FUNCTION_NAME=$(basename "$PWD")
fi

if [[ -z "${S3_BUCKET}" ]]; then
  read -p "Enter environment: " environment
  if [[ ! -z "${environment}" ]]; then
    export S3_BUCKET="cdp-${environment}-lambda-functions"
  else
    echo "Environment not set"
    exit 1
  fi
fi

aws s3 cp output/"${FUNCTION_NAME}".zip s3://"${S3_BUCKET}/${FUNCTION_NAME}".zip
aws s3 cp --content-type text/plain output/"${FUNCTION_NAME}".zip.base64sha256 s3://"${S3_BUCKET}"/"${FUNCTION_NAME}".zip.base64sha256
