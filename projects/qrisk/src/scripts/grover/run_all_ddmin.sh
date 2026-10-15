#!/bin/bash
# Run the Grover-3 DDMin batch on all 3 backends in parallel and wait for them.
# Usage: scripts/grover/run_all_ddmin.sh [--push]
#   --push  commit the new reports under data/artifacts/ and push (the weekly cron mode)
# Logs: data/run_logs/<timestamp>/{fez,marrakesh,kingston}.log

set -uo pipefail
cd "$(dirname "$0")/../.." || exit 1

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_DIR="data/run_logs/$TIMESTAMP"
mkdir -p "$LOG_DIR"

echo "Starting delta debug experiments (logs in $LOG_DIR)..."
pids=()
for backend in ibm_fez ibm_marrakesh ibm_kingston; do
  .venv/bin/python -m scripts.grover.generate_and_run_grover3 --run-only --backend "$backend" \
    > "$LOG_DIR/${backend#ibm_}.log" 2>&1 &
  pids+=($!)
  echo "  $backend PID=$!"
done
wait "${pids[@]}"

if [[ "${1:-}" == "--push" ]]; then
  git add data/artifacts/ "$LOG_DIR"
  git commit -m "update data $TIMESTAMP" || true
  git push || true
fi
