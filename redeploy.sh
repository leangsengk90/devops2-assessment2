#!/usr/bin/env bash
# Redeploy the microservices only (remote-state and infrastructures are left as they are).
# For each service: apply Terraform if its code changed (e.g. a new image tag),
# otherwise force ECS to start fresh tasks, then wait until every service is healthy.
#
# Pushing a change to this file on main runs it in GitHub Actions (Rebuild prod workflow).
# Change note (edit to trigger a redeploy): initial
set -euo pipefail
cd "$(dirname "$0")"
source .github/scripts/timeline.sh

AWS_REGION=${AWS_REGION:-ap-southeast-2}
export AWS_REGION AWS_DEFAULT_REGION=$AWS_REGION
TF_WORKSPACE_NAME=${TF_WORKSPACE_NAME:-prod}
SERVICES=${SERVICES:-auth messenger profile finance share}
VARS=$PWD/variables/global.tfvars

tf_init() { # dir
  terraform -chdir="$1" init -input=false
  terraform -chdir="$1" workspace select -or-create "$TF_WORKSPACE_NAME"
}

tf_init main/infrastructures
API_ENDPOINT=$(terraform -chdir=main/infrastructures output -raw api_gateway_endpoint)
[ -n "${GITHUB_ENV:-}" ] && echo "API_ENDPOINT=$API_ENDPOINT" >> "$GITHUB_ENV"

phase_begin "Redeploy deployments"
for s in $SERVICES; do
  d=main/deployments/$s
  tf_init "$d"
  plan=${RUNNER_TEMP:-${TMPDIR:-/tmp}}/$s-redeploy.plan
  rc=0
  terraform -chdir="$d" plan -input=false -var-file="$VARS" -detailed-exitcode -out="$plan" || rc=$?
  case $rc in
    2) echo "$s: Terraform changes found, applying"
       terraform -chdir="$d" apply -input=false "$plan" ;;
    0) echo "$s: no Terraform changes, forcing a new deployment"
       aws ecs update-service \
         --cluster "devops2-g4-$s-cluster-$TF_WORKSPACE_NAME" \
         --service "devops2-g4-$s-service-$TF_WORKSPACE_NAME" \
         --force-new-deployment --query 'service.serviceName' --output text ;;
    *) exit $rc ;;
  esac
done
phase_end

phase_begin "Wait until healthy"
for s in $SERVICES; do
  aws ecs wait services-stable \
    --cluster "devops2-g4-$s-cluster-$TF_WORKSPACE_NAME" \
    --services "devops2-g4-$s-service-$TF_WORKSPACE_NAME"
done
phase_end

echo "Redeploy complete. API endpoint: $API_ENDPOINT"
