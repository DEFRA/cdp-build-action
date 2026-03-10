#!/bin/bash

if [[ -z "${FUNCTION_NAME}" ]]; then
  export FUNCTION_NAME=$(basename "$PWD")
fi

dist_folder="./output"
python_version=$(uv run python --version | awk '{print $2}')

rm -rf "${dist_folder}/*.zip*"
mkdir -p ${dist_folder}
uv export --frozen --no-dev --no-editable -o requirements.txt

uv pip install \
   --no-installer-metadata \
   --no-compile-bytecode \
   --python-platform x86_64-manylinux2014 \
   --python ${python_version} \
   --target ${dist_folder} \
   -r requirements.txt

rm requirements.txt

cp config.py ${dist_folder}
cp handler.py ${dist_folder}
cp -r modules ${dist_folder}

cd ${dist_folder}
zip -r "${FUNCTION_NAME}.zip" .
cd ..

sha256sum ${dist_folder}/"${FUNCTION_NAME}.zip" | awk '{print $1}' > ${dist_folder}/"${FUNCTION_NAME}".zip.sha256
cat ${dist_folder}/"${FUNCTION_NAME}.zip.sha256" | xxd -r -p | base64 > ${dist_folder}/"${FUNCTION_NAME}".zip.base64sha256
