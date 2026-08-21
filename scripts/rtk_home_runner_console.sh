#!/usr/bin/env bash
set -Eeuo pipefail

# Persistent launcher for the already-configured RTK GitHub self-hosted runner.
# It keeps official run.sh in the foreground and mirrors RTK scientific progress
# from $HOME/.rtk-runner-state/live.log into the same Ubuntu terminal.

RUNNER_DIR="${RTK_RUNNER_DIR:-$PWD}"
STATE_ROOT="${RTK_STATE_ROOT:-$HOME/.rtk-runner-state}"
GLOBAL_LOG="$STATE_ROOT/live.log"

if [[ ! -x "$RUNNER_DIR/run.sh" ]]; then
  echo "[RTK RUNNER] run.sh not found in: $RUNNER_DIR" >&2
  echo "[RTK RUNNER] cd to the configured GitHub Actions runner directory, then run this launcher." >&2
  exit 2
fi

mkdir -p "$STATE_ROOT"
touch "$GLOBAL_LOG"

echo "============================================================"
echo " RTK HOME COMPUTE NODE"
echo " runner dir : $RUNNER_DIR"
echo " host       : $(hostname)"
echo " logical CPU: $(nproc)"
echo " state      : $STATE_ROOT"
echo " progress   : $GLOBAL_LOG"
echo "============================================================"
echo "[RTK RUNNER] Waiting for GitHub jobs. Ctrl+C stops the runner; checkpoints remain on disk."

tail -n 30 -F "$GLOBAL_LOG" 2>/dev/null &
TAIL_PID=$!

cleanup() {
  kill "$TAIL_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

cd "$RUNNER_DIR"
./run.sh
status=$?
cleanup
exit "$status"
