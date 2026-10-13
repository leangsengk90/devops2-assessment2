# Phase timing helpers for the rebuild-prod workflow.
# Usage inside a step:  source .github/scripts/timeline.sh; phase_begin "Create infrastructures"
# The phase end (and its ok/failed status) is recorded automatically when the step's shell exits.

TIMELINE="$RUNNER_TEMP/timeline.csv"

phase_begin() {
  PHASE_NAME="$1"
  PHASE_T0=$(date +%s)
  echo "⏱ [$(date '+%H:%M:%S')] $PHASE_NAME started"
  trap 'phase_end $?' EXIT
}

phase_end() {
  local rc=$1 t1 status=ok
  t1=$(date +%s)
  [ "$rc" = 0 ] || status=failed
  echo "$PHASE_NAME,$(date -d "@$PHASE_T0" -Iseconds),$(date -d "@$t1" -Iseconds),$((t1 - PHASE_T0)),$status" >> "$TIMELINE"
  echo "⏱ [$(date '+%H:%M:%S')] $PHASE_NAME finished in $((t1 - PHASE_T0))s ($status)"
}
