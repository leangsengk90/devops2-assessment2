#!/usr/bin/env bash
# Full rebuild of prod: destroy deployments -> infrastructures -> remote-state,
# then recreate remote-state -> infrastructures -> deployments and wait until healthy.
# ECR repositories and their images are never destroyed.
# 6
# Pushing a change to this file on main runs it in GitHub Actions (Rebuild prod workflow).
# Change note (edit to trigger a rebuild): initial
set -euo pipefail
cd "$(dirname "$0")"
source .github/scripts/timeline.sh

AWS_REGION=${AWS_REGION:-ap-southeast-2}
export AWS_REGION AWS_DEFAULT_REGION=$AWS_REGION
TF_WORKSPACE_NAME=${TF_WORKSPACE_NAME:-prod}
STATE_BUCKET=${STATE_BUCKET:-devops2-g4-remote-state-029637202701}
SERVICES=${SERVICES:-auth messenger profile finance share}
ECR_SERVICES=${ECR_SERVICES:-api1 auth messenger profile finance share}
VARS=$PWD/variables/global.tfvars
INFRA_STATE=${RUNNER_TEMP:-${TMPDIR:-/tmp}}/infrastructures.tfstate
rm -f "$INFRA_STATE"

tf_init() { # dir [extra init args]
  terraform -chdir="$1" init -input=false "${@:2}"
  terraform -chdir="$1" workspace select -or-create "$TF_WORKSPACE_NAME"
}

# ---------------- destroy ----------------
if aws s3api head-bucket --bucket "$STATE_BUCKET" 2>/dev/null; then
  phase_begin "Destroy deployments"
  for s in $SERVICES; do
    tf_init "main/deployments/$s"
    terraform -chdir="main/deployments/$s" destroy -auto-approve -input=false -var-file="$VARS"
  done
  phase_end

  phase_begin "Destroy infrastructures"
  d=main/infrastructures
  tf_init $d
  targets=()
  while IFS= read -r r; do targets+=("$r"); done < <(terraform -chdir=$d state list | grep -vE '^module\.ecr_|(^|\.)data\.' || true)
  if [ ${#targets[@]} -gt 0 ]; then
    terraform -chdir=$d destroy -auto-approve -input=false -var-file="$VARS" "${targets[@]/#/-target=}"
  fi
  # The state bucket is about to be deleted: keep the state that still tracks the ECR repos.
  terraform -chdir=$d state pull > "$INFRA_STATE"
  phase_end

  phase_begin "Destroy remote-state"
  tf_init main/remote-state
  terraform -chdir=main/remote-state destroy -auto-approve -input=false -var-file="$VARS"
  phase_end
else
  echo "State bucket $STATE_BUCKET not found: skipping destroy phases."
fi

# ---------------- create ----------------
phase_begin "Create remote-state"
tf_init main/remote-state
# A just-deleted bucket name can take a moment to become reusable.
for attempt in 1 2 3 4 5 6 7 8 9 10; do
  if terraform -chdir=main/remote-state apply -auto-approve -input=false -var-file="$VARS"; then break; fi
  [ $attempt = 10 ] && exit 1
  echo "Retrying in 20s (attempt $attempt failed)"; sleep 20
done
phase_end

phase_begin "Create infrastructures"
d=main/infrastructures
tf_init $d -reconfigure
if [ -s "$INFRA_STATE" ]; then
  terraform -chdir=$d state push "$INFRA_STATE"
else
  # No carried-over state: adopt the ECR repositories that already exist.
  for s in $ECR_SERVICES; do
    repo=devops2-g4-$s-$TF_WORKSPACE_NAME
    if aws ecr describe-repositories --repository-names "$repo" >/dev/null 2>&1; then
      terraform -chdir=$d import -input=false -var-file="$VARS" "module.ecr_$s.aws_ecr_repository.this" "$repo"
      terraform -chdir=$d import -input=false -var-file="$VARS" "module.ecr_$s.aws_ecr_lifecycle_policy.this[0]" "$repo" || true
    fi
  done
fi
terraform -chdir=$d apply -auto-approve -input=false -var-file="$VARS"
API_ENDPOINT=$(terraform -chdir=$d output -raw api_gateway_endpoint)
[ -n "${GITHUB_ENV:-}" ] && echo "API_ENDPOINT=$API_ENDPOINT" >> "$GITHUB_ENV"
phase_end

phase_begin "Create deployments"
for s in $SERVICES; do
  tf_init "main/deployments/$s" -reconfigure
  terraform -chdir="main/deployments/$s" apply -auto-approve -input=false -var-file="$VARS"
done
phase_end

phase_begin "Wait until healthy"
for s in $SERVICES; do
  aws ecs wait services-stable \
    --cluster "devops2-g4-$s-cluster-$TF_WORKSPACE_NAME" \
    --services "devops2-g4-$s-service-$TF_WORKSPACE_NAME"
done
phase_end

echo "Rebuild complete. API endpoint: $API_ENDPOINT"
