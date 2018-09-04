#!/bin/bash

set -ex
set -o pipefail

echo "Declaring environment variables"

declare_env_variables() {
  DEPLOYMENT_ENVIRONMENT="staging"
  RESERVED_IP=${STAGING_RESERVED_IP}
  PROJECT="andela-learning"
  PACKER_IMG_TAG=$(cat ~/activo-api/workspace/output)

  if [ "$CIRCLE_BRANCH" == 'master' ]; then
    DEPLOYMENT_ENVIRONMENT="production"
    RESERVED_IP=${PRODUCTION_RESERVED_IP}
  fi

  if [[ "$CIRCLE_BRANCH" =~ 'sandbox' ]]; then
    DEPLOYMENT_ENVIRONMENT="sandbox"
    RESERVED_IP=${SANDBOX_RESERVED_IP}
  fi

  EMOJIS=(":celebrate:"  ":party_dinosaur:"  ":andela:" ":aw-yeah:" ":carlton-dance:" ":partyparrot:" ":dancing-penguin:" ":aww-yeah-remix:" )
  RANDOM=$$$(date +%s)
  EMOJI=${EMOJIS[$RANDOM % ${#EMOJIS[@]} ]}
  COMMIT_LINK="https://github.com/${CIRCLE_PROJECT_USERNAME}/${CIRCLE_PROJECT_REPONAME}/commit/${CIRCLE_SHA1}"
  DEPLOYMENT_TEXT="Tag: ${PACKER_IMG_TAG} has just been deployed as the latest ${PROJECT} in ${DEPLOYMENT_ENVIRONMENT}  $COMMIT_LINK "
  DEPLOYMENT_CHANNEL=${SLACK_CHANNEL}
  IMG_TAG="$(git rev-parse --short HEAD)"
  SLACK_DEPLOYMENT_TEXT="Git Commit Tag: <$COMMIT_LINK|${IMG_TAG}> has just been deployed to *${PROJECT}* in *${DEPLOYMENT_ENVIRONMENT}* ${EMOJI}"
}

check_out_infrastructure_code() {
  echo "Checking infrastructure code"

  mkdir -p /home/circleci/activo-infra

  if [ "$CIRCLE_BRANCH" == "master" ]; then
    git clone -b master ${INFRASTRUCTURE_REPO} /home/circleci/activo-infra
  else
    git clone -b develop ${INFRASTRUCTURE_REPO} /home/circleci/activo-infra
  fi
}

generate_service_account() {
  touch /home/circleci/activo-infra/shared/account.json
  echo ${SERVICE_ACCOUNT} > /home/circleci/activo-infra/shared/account.json
}

setup_ssl_files() {
  if gcloud auth activate-service-account --key-file=/home/circleci/activo-infra/shared/account.json; then
    gsutil cp gs://${GCLOUD_ACTIVO_BUCKET}/ssl/andela_certificate.crt /home/circleci/activo-infra/shared/andela_certificate.crt
    gsutil cp gs://${GCLOUD_ACTIVO_BUCKET}/ssl/andela_key.key /home/circleci/activo-infra/shared/andela_key.key
  fi
}

initialise_terraform() {
  echo "Initializing terraform"

  pushd /home/circleci/activo-infra/activo/api
    export TF_VAR_state_path="api/state/${DEPLOYMENT_ENVIRONMENT}/terraform.tfstate"
    export TF_VAR_project=${GCLOUD_ACTIVO_PROJECT}
    export TF_VAR_bucket=${GCLOUD_ACTIVO_BUCKET}

    terraform init -backend-config="path=${TF_VAR_state_path}" -backend-config="project=${TF_VAR_project}" -backend-config="bucket=${TF_VAR_bucket}" -var="api_env_name=${DEPLOYMENT_ENVIRONMENT}" -var="api_flask_env=${FLASK_ENV}" -var="api_disk_image=${PACKER_IMG_TAG}"  -var="api_reserved_env_ip=${RESERVED_IP}"
  popd
}

build_infrastructure() {
  echo "Building activo api infrastructure and deploying activo api application"

  pushd /home/circleci/activo-infra/activo/api
    touch terraform_output.log
    if [ "$DEPLOYMENT_ENVIRONMENT" == "production" ]; then
      terraform apply --parallelism=1 -var="api_state_path=${TF_VAR_state_path}" -var="api_project_id=${TF_VAR_project}" -var="api_bucket=${TF_VAR_bucket}" -var="api_env_name=${DEPLOYMENT_ENVIRONMENT}" -var="api_flask_env=${FLASK_ENV}" -var="api_disk_image=${PACKER_IMG_TAG}" -var="api_reserved_env_ip=${RESERVED_IP}" \
      -var="api_service_account_email=${SERVICE_ACCOUNT_EMAIL}" -var="api_max_instances=${PRODUCTION_MAX_INSTANCES}" -var="api_slack_channel=${SLACK_CHANNEL}" -var="api_slack_webhook_url=${SLACK_CHANNEL_HOOK}" -var="user_microservice_api_url=${USER_MICROSERVICE_API_URL}" \
      -var="cloudinary_cloud_name=${CLOUDINARY_CLOUD_NAME}" -var="cloudinary_api_secret=${CLOUDINARY_API_SECRET}" -var="cloudinary_api_key=${CLOUDINARY_API_KEY}" -var="api_jwt_public_key=${JWT_PUBLIC_KEY}" -var="api_jwt_public_key_staging=${JWT_PUBLIC_KEY_STAGING}" -var="user_microservice_api_token=${USER_MICROSERVICE_API_TOKEN}" 2>&1 | tee terraform_output.log
    else
      terraform apply --parallelism=1 -var="api_state_path=${TF_VAR_state_path}" -var="api_project_id=${TF_VAR_project}" -var="api_bucket=${TF_VAR_bucket}" -var="api_env_name=${DEPLOYMENT_ENVIRONMENT}" -var="api_flask_env=${FLASK_ENV}" -var="api_disk_image=${PACKER_IMG_TAG}" \
      -var="api_reserved_env_ip=${RESERVED_IP}" -var="api_service_account_email=${SERVICE_ACCOUNT_EMAIL}" -var="api_slack_channel=${SLACK_CHANNEL}" -var="api_slack_webhook_url=${SLACK_CHANNEL_HOOK}" -var="user_microservice_api_url=${USER_MICROSERVICE_API_URL}" \
      -var="cloudinary_cloud_name=${CLOUDINARY_CLOUD_NAME}" -var="cloudinary_api_secret=${CLOUDINARY_API_SECRET}" -var="cloudinary_api_key=${CLOUDINARY_API_KEY}" -var="api_jwt_public_key=${JWT_PUBLIC_KEY}" -var="api_jwt_public_key_staging=${JWT_PUBLIC_KEY_STAGING}" -var="user_microservice_api_token=${USER_MICROSERVICE_API_TOKEN}" 2>&1 | tee terraform_output.log
    fi
  popd
}

run_rolling_update() {
  echo "Running rolling update on application"

  INSTANCE_MANAGER="$(grep 'instance-group-manager = ' /home/circleci/activo-infra/activo/api/terraform_output.log | cut -d' ' -f3)"
  INSTANCE_TEMPLATE="$(grep 'new-instance-template = ' /home/circleci/activo-infra/activo/api/terraform_output.log | cut -d' ' -f3)"

  if gcloud auth activate-service-account --key-file=/home/circleci/activo-infra/shared/account.json; then
    gcloud config set project ${GCLOUD_ACTIVO_PROJECT}
    gcloud beta compute instance-groups managed rolling-action start-update ${INSTANCE_MANAGER} --version template=${INSTANCE_TEMPLATE} --max-surge 2 --max-unavailable 1 --zone europe-west1-b --min-ready 3m
  fi
}

notify_team_via_slack() {
  echo "Sending success message to slack"

  curl -X POST --data-urlencode \
  "payload={\"channel\": \"${DEPLOYMENT_CHANNEL}\", \"username\": \"DeployNotification\", \"text\": \"${SLACK_DEPLOYMENT_TEXT}\", \"icon_emoji\": \":rocket:\"}" \
  "${SLACK_CHANNEL_HOOK}"
}

main() {
  echo "Deployment script invoked at $(date)" >> /tmp/script.log

  declare_env_variables
  check_out_infrastructure_code
  generate_service_account
  setup_ssl_files
  initialise_terraform
  build_infrastructure
  run_rolling_update
  notify_team_via_slack 
}

main "$@"
