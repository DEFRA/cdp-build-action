#!/bin/bash
set -e

cd "$1"

terraform plan -input=false -var-file "environments/${ENVIRONMENT}/terraform.tfvars" -compact-warnings -detailed-exitcode -out="${ENVIRONMENT}.plan.file"
TF_FORCE_COLOR=1 terraform show "${ENVIRONMENT}.plan.file" | tee "${ENVIRONMENT}.tf_plan.txt"
EXITCODE=$?

# Check the file size of the plan output file
FILE_SIZE=$(wc -c < "${ENVIRONMENT}.tf_plan.txt")
MAX_SIZE=131072  # 128 KiB

if [ "$FILE_SIZE" -gt "$MAX_SIZE" ]; then
  echo "plan_is_large=true" >> "$GITHUB_OUTPUT"
  KB_SIZE=$(($FILE_SIZE / 1024))
  echo "❗ **Terraform plan output for ${ENVIRONMENT} environment is too large (${KB_SIZE} KiB)**." > "${ENVIRONMENT}.tf_plan.txt"
  echo "Please check the full plan in the [GitHub Actions run]($GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID)" >> "${ENVIRONMENT}.tf_plan.txt"
else
  echo "plan_is_large=false" >> "$GITHUB_OUTPUT"
fi

{
  printf "plan_text<<PLAN_OUTPUT\n"
  cat "${ENVIRONMENT}.tf_plan.txt"
  printf "\nPLAN_OUTPUT\n"
} >> "$GITHUB_OUTPUT"

echo "exitcode=$EXITCODE" >> "$GITHUB_OUTPUT"

exit $EXITCODE
