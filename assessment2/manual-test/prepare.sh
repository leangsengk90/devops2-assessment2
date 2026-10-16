#!/usr/bin/env bash
# Empty the prod environment before the FIRST manual run: destroy the Terraform-managed
# deployments -> infrastructures (except ECR) -> remote-state, exactly like the destroy half of rebuild.sh.
# ECR repositories and their images are kept, so the manually built services can pull them.
# Run from anywhere:  CONFIRM=destroy ./prepare.sh
set -euo pipefail
cd "$(dirname "$0")/../.."          # repository root

if [ "${CONFIRM:-}" != destroy ]; then
  echo "This destroys the Terraform-managed prod environment (ECR is kept). Run with CONFIRM=destroy." >&2
  exit 1
fi

export AWS_REGION=ap-southeast-2 AWS_DEFAULT_REGION=ap-southeast-2
WS=prod
VARS=$PWD/variables/global.tfvars
STATE_BUCKET=devops2-g4-remote-state-029637202701

tf_init() { terraform -chdir="$1" init -input=false -reconfigure >/dev/null && terraform -chdir="$1" workspace select -or-create "$WS"; }

if ! aws s3api head-bucket --bucket "$STATE_BUCKET" 2>/dev/null; then
  echo "State bucket not found: the Terraform environment is already gone. Nothing to do."; exit 0
fi

for s in auth messenger profile finance share; do
  tf_init "main/deployments/$s"
  terraform -chdir="main/deployments/$s" destroy -auto-approve -input=false -var-file="$VARS"
done

d=main/infrastructures
tf_init $d
targets=()
while IFS= read -r r; do targets+=("$r"); done < <(terraform -chdir=$d state list | grep -vE '^module\.ecr_|(^|\.)data\.' || true)
[ ${#targets[@]} -gt 0 ] && terraform -chdir=$d destroy -auto-approve -input=false -var-file="$VARS" "${targets[@]/#/-target=}"

tf_init main/remote-state
terraform -chdir=main/remote-state destroy -auto-approve -input=false -var-file="$VARS"

echo "Done. The account is empty except for the ECR repositories. Start manual run 1."
