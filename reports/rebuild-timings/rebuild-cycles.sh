#!/bin/bash
# Destroy and recreate remote-state -> infrastructures -> deployments N times, timing every phase.
# ECR repositories (and their images) are kept across cycles; their state is carried over by
# pulling the infrastructures state before the state bucket is destroyed and pushing it back after.
#
# Usage: rebuild-cycles.sh FIRST_CYCLE LAST_CYCLE
set -u

ROOT=/Users/kaoleangseng/Downloads/devops2-assessment2-main
OUT=$ROOT/reports/rebuild-timings
VARS=$ROOT/variables/global.tfvars
REGION=ap-southeast-2
SERVICES="auth messenger profile finance share"

CSV=$OUT/timings.csv
SVC_CSV=$OUT/service-health.csv
mkdir -p "$OUT/logs" "$OUT/state"
[ -f "$CSV" ] || echo "cycle,action,stack,step,start,end,seconds,exit_code" > "$CSV"
[ -f "$SVC_CSV" ] || echo "cycle,service,service_created,steady_state,seconds_to_healthy,http_code" > "$SVC_CSV"

iso() { date -r "$1" '+%Y-%m-%d %H:%M:%S'; }
log() { echo "[$(date '+%H:%M:%S')] $*"; }

# run CYCLE ACTION STACK STEP DIR CMD... -> times CMD, appends a CSV row, returns its exit code
run() {
  local c=$1 a=$2 s=$3 st=$4 d=$5; shift 5
  local t0 t1 rc logf=$OUT/logs/c$(printf %02d "$c")-$a-$s-$st.log
  t0=$(date +%s)
  (cd "$d" && "$@") >"$logf" 2>&1; rc=$?
  t1=$(date +%s)
  echo "$c,$a,$s,$st,$(iso "$t0"),$(iso "$t1"),$((t1 - t0)),$rc" >> "$CSV"
  log "cycle $c $a $s $st: $((t1 - t0))s (exit $rc)"
  return $rc
}

fail() { log "ABORT: $*"; exit 1; }

for ((c = $1; c <= $2; c++)); do
  log "===== cycle $c start ====="
  CYCLE_T0=$(date +%s)

  # ---------- destroy: deployments -> infrastructures (except ECR) -> remote-state ----------
  for s in $SERVICES; do
    run "$c" destroy "$s" destroy "$ROOT/main/deployments/$s" \
      terraform destroy -auto-approve -input=false -var-file="$VARS" || fail "destroy $s"
  done

  INFRA=$ROOT/main/infrastructures
  TARGETS=$(cd "$INFRA" && terraform state list | grep -vE '^module\.ecr_|(^|\.)data\.' | sed 's/^/-target=/')
  [ -n "$TARGETS" ] || fail "no infrastructure targets found"
  # shellcheck disable=SC2086
  run "$c" destroy infrastructures destroy "$INFRA" \
    terraform destroy -auto-approve -input=false -var-file="$VARS" $TARGETS || fail "destroy infrastructures"
  (cd "$INFRA" && terraform state pull) > "$OUT/state/infra-c$c.tfstate" || fail "state pull"

  run "$c" destroy remote-state destroy "$ROOT/main/remote-state" \
    terraform destroy -auto-approve -input=false -var-file="$VARS" || fail "destroy remote-state"

  # ---------- create: remote-state -> infrastructures -> deployments ----------
  RS=$ROOT/main/remote-state
  ok=0
  for attempt in 1 2 3 4 5 6 7 8 9 10; do
    run "$c" create remote-state plan "$RS" \
      terraform plan -input=false -var-file="$VARS" -out="$ROOT/plans/remote-state-prod.plan" || fail "plan remote-state"
    if run "$c" create remote-state "apply-try$attempt" "$RS" \
        terraform apply -input=false "$ROOT/plans/remote-state-prod.plan"; then ok=1; break; fi
    sleep 20 # a just-deleted bucket name can take a moment to become reusable
  done
  [ $ok = 1 ] || fail "apply remote-state"

  (cd "$INFRA" && { terraform workspace select prod >/dev/null 2>&1 || terraform workspace new prod >/dev/null; } \
    && terraform state push "$OUT/state/infra-c$c.tfstate") > "$OUT/logs/c$(printf %02d "$c")-state-push.log" 2>&1 \
    || fail "state push"
  run "$c" create infrastructures plan "$INFRA" \
    terraform plan -input=false -var-file="$VARS" -out="$ROOT/plans/infrastructure-prod.plan" || fail "plan infrastructures"
  run "$c" create infrastructures apply "$INFRA" \
    terraform apply -input=false "$ROOT/plans/infrastructure-prod.plan" || fail "apply infrastructures"
  API=$(cd "$INFRA" && terraform output -raw api_gateway_endpoint)

  for s in $SERVICES; do
    D=$ROOT/main/deployments/$s
    (cd "$D" && { terraform workspace select prod >/dev/null 2>&1 || terraform workspace new prod >/dev/null; })
    run "$c" create "$s" plan "$D" \
      terraform plan -input=false -var-file="$VARS" -out="$ROOT/plans/$s-prod.plan" || fail "plan $s"
    run "$c" create "$s" apply "$D" \
      terraform apply -input=false "$ROOT/plans/$s-prod.plan" || fail "apply $s"
  done

  # ---------- wait until every ECS service is healthy, then record per-service health ----------
  for s in $SERVICES; do
    run "$c" create "$s" wait-healthy "$ROOT" \
      aws ecs wait services-stable --region $REGION \
      --cluster "devops2-g4-$s-cluster-prod" --services "devops2-g4-$s-service-prod" || log "WARN: $s not stable"
  done
  for s in $SERVICES; do
    read -r created steady < <(aws ecs describe-services --region $REGION \
      --cluster "devops2-g4-$s-cluster-prod" --services "devops2-g4-$s-service-prod" \
      --query 'services[0].[createdAt, events[?contains(message, `steady state`)]|[-1].createdAt]' --output text)
    secs=$(python3 -c "from datetime import datetime as d; import sys; print(round((d.fromisoformat(sys.argv[2])-d.fromisoformat(sys.argv[1])).total_seconds()))" "$created" "$steady" 2>/dev/null || echo "")
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$API/$s")
    echo "$c,$s,$created,$steady,$secs,$code" >> "$SVC_CSV"
  done

  CYCLE_T1=$(date +%s)
  echo "$c,cycle,all,total,$(iso "$CYCLE_T0"),$(iso "$CYCLE_T1"),$((CYCLE_T1 - CYCLE_T0)),0" >> "$CSV"
  log "===== cycle $c done in $((CYCLE_T1 - CYCLE_T0))s ====="
done
log "ALL DONE"
