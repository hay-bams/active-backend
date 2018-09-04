#!/bin/bash

set -ex
set -o pipefail

echo "building the packer image"

declare_env_variables() {
  DEPLOYMENT_ENVIRONMENT="staging"
  PACKER_IMG_TAG=""
  if [ "$CIRCLE_BRANCH" == 'master' ]; then
    DEPLOYMENT_ENVIRONMENT="production"
    RESERVED_IP=${PRODUCTION_RESERVED_IP}
  fi

  if [[ "$CIRCLE_BRANCH" =~ 'sandbox' ]]; then
    DEPLOYMENT_ENVIRONMENT="sandbox"
    RESERVED_IP=${SANDBOX_RESERVED_IP}
  fi
}

generate_service_account() {
  touch /home/circleci/activo-infra/shared/account.json
  echo ${SERVICE_ACCOUNT} > /home/circleci/activo-infra/shared/account.json
}

build_packer_image() {
  echo "Rebuilding the packer image"

  pushd /home/circleci/activo-infra/packer/api
    touch packer_output.log
    ENV_NAME="$DEPLOYMENT_ENVIRONMENT" HOME_PATH="/home/circleci/activo-api" PROJECT_ID="$GCLOUD_ACTIVO_PROJECT" packer build packer.json 2>&1 | tee packer_output.log
    PACKER_IMG_TAG="$(grep 'A disk image was created:' packer_output.log | cut -d' ' -f8)"
  popd
  mkdir -p workspace
  echo $PACKER_IMG_TAG > ~/activo-api/workspace/output
  cat ~/activo-api/workspace/output
}

check_out_infrastructure_code() {
  echo "Checking the infrastructure code"

  mkdir -p /home/circleci/activo-infra

  if [ "$CIRCLE_BRANCH" == "master" ]; then
    git clone -b master ${INFRASTRUCTURE_REPO} /home/circleci/activo-infra
  else
    git clone -b develop ${INFRASTRUCTURE_REPO} /home/circleci/activo-infra
  fi
}

main() {
  check_out_infrastructure_code
  declare_env_variables
  generate_service_account
  build_packer_image
}

main "@$"
