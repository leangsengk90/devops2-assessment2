# Phase timing helpers for rebuild.sh / redeploy.sh.
# Usage:  source .github/scripts/timeline.sh
#         phase_begin "Create infrastructures"; ...; phase_end
# If the script exits while a phase is open, that phase is recorded as failed.

TIMELINE="${TIMELINE:-${RUNNER_TEMP:-${TMPDIR:-/tmp}}/timeline.csv}"
PHASE_NAME=""

_now() { date +%Y-%m-%dT%H:%M:%S%z; }

phase_begin() {
  PHASE_NAME="$1"
  PHASE_START=$(_now)
  PHASE_T0=$(date +%s)
  echo "⏱ [$(date +%H:%M:%S)] $PHASE_NAME started"
}

phase_end() {
  local status=${1:-ok} t1
  t1=$(date +%s)
  echo "$PHASE_NAME,$PHASE_START,$(_now),$((t1 - PHASE_T0)),$status" >> "$TIMELINE"
  echo "⏱ [$(date +%H:%M:%S)] $PHASE_NAME finished in $((t1 - PHASE_T0))s ($status)"
  PHASE_NAME=""
}

trap '[ -n "$PHASE_NAME" ] && phase_end failed' EXIT
