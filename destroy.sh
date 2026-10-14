#!/usr/bin/env bash
# Destroy everything in prod: deployments -> infrastructures (including the ECR repositories and
# all their images) -> remote-state. Nothing is recreated; run rebuild.sh to bring prod back
# (the images then have to be built and pushed again before the services can start).
#
# Pushing a change to this file on main runs it in GitHub Actions (Rebuild prod workflow).
# Run locally with CONFIRM=destroy ./destroy.sh
# Change note (edit to trigger a destroy): initial
set -euo pipefail
cd "$(dirname "$0")"

if [ -z "${GITHUB_ACTIONS:-}" ] && [ "${CONFIRM:-}" != destroy ]; then
  echo "This deletes all of prod, including the ECR images. Run with CONFIRM=destroy to go ahead." >&2
  exit 1
fi

source .github/scripts/timeline.sh

AWS_REGION=${AWS_REGION:-ap-southeast-2}
export AWS_REGION AWS_DEFAULT_REGION=$AWS_REGION
TF_WORKSPACE_NAME=${TF_WORKSPACE_NAME:-prod}
STATE_BUCKET=${STATE_BUCKET:-devops2-g4-remote-state-029637202701}
SERVICES=${SERVICES:-auth messenger profile finance share}
VARS=$PWD/variables/global.tfvars

tf_init() { # dir
  terraform -chdir="$1" init -input=false -reconfigure
  terraform -chdir="$1" workspace select -or-create "$TF_WORKSPACE_NAME"
}

if ! aws s3api head-bucket --bucket "$STATE_BUCKET" 2>/dev/null; then
  echo "State bucket $STATE_BUCKET not found: prod is already destroyed."
  exit 0
fi

phase_begin "Destroy deployments"
for s in $SERVICES; do
  tf_init "main/deployments/$s"
  terraform -chdir="main/deployments/$s" destroy -auto-approve -input=false -var-file="$VARS"
done
phase_end

# Full destroy: the ECR repositories have force_delete = true, so their images go with them.
phase_begin "Destroy infrastructures"
tf_init main/infrastructures
terraform -chdir=main/infrastructures destroy -auto-approve -input=false -var-file="$VARS"
phase_end

phase_begin "Destroy remote-state"
tf_init main/remote-state
terraform -chdir=main/remote-state destroy -auto-approve -input=false -var-file="$VARS"
phase_end

echo "Destroy complete: prod, its ECR images and the state bucket are gone."
