#!/usr/bin/env bash
# Run the full cross-algorithm experiment (preflight -> probe -> Exp 1 -> Exp 2).
#
#   bash scripts/xalg/run_all.sh ibm_fez              # real hardware, 40-min QPU cap
#   BUDGET_MIN=50 bash scripts/xalg/run_all.sh ibm_fez
#   HARDWARE=emulate bash scripts/xalg/run_all.sh ibm_fez   # offline dry run, no IBM
#   RESULTS_DIR=/tmp/xalg HARDWARE=emulate bash scripts/xalg/run_all.sh ibm_fez
#
# Results go to data/results/xalg (ibm) or data/results/xalg_dryrun (emulate)
# unless RESULTS_DIR is set.
#
# Budget: BUDGET_MIN (default 40) is the TOTAL QPU cap across all steps.
# Exp 1 may use at most BUDGET_MIN - EXP2_RESERVE_MIN (default 12), so the
# dose-response experiment always has QPU time left.
#
# Pauses for confirmation before every step that uses QPU time.
# Re-running resumes: finished DDMin runs and variant sets are skipped.
set -uo pipefail

BACKEND="${1:-ibm_fez}"
BUDGET_MIN="${BUDGET_MIN:-40}"
HARDWARE="${HARDWARE:-ibm}"
RUNS="${RUNS:-2}"
EXP2_RESERVE_MIN="${EXP2_RESERVE_MIN:-12}"
PARALLEL="${PARALLEL:-4}"
EXP1_BUDGET_MIN=$(python -c "print(max(1, $BUDGET_MIN - $EXP2_RESERVE_MIN))")
if [[ -n "${RESULTS_DIR:-}" ]]; then RESULTS_DIR=$(mkdir -p "$RESULTS_DIR" && cd "$RESULTS_DIR" && pwd) || exit 1; fi
cd "$(dirname "$0")/../.."

if [[ -n "${RESULTS_DIR:-}" ]]; then RESULTS="$RESULTS_DIR"
elif [[ "$HARDWARE" == "emulate" ]]; then RESULTS="data/results/xalg_dryrun"
else RESULTS="data/results/xalg"; fi
COMMON=(--backend "$BACKEND" --hardware "$HARDWARE" --results-dir "$RESULTS")

confirm() {
  [[ "$HARDWARE" == "emulate" ]] && return 0
  read -r -p "$1 [y/N] " ans
  [[ "$ans" == "y" || "$ans" == "Y" ]]
}

echo "== Step 1: compile + simulator preflight (no QPU) =="
python -m scripts.xalg.prepare "${COMMON[@]}" || exit 1

if [[ "$HARDWARE" == "ibm" ]]; then
  echo; echo "== Step 2: one-job cost probe (~5-10 s QPU) =="
  confirm "Submit the probe job to $BACKEND?" || exit 0
  python -m scripts.xalg.probe "${COMMON[@]}" --budget-min "$BUDGET_MIN" || exit 1
fi

echo; echo "== Step 3: Exp 1 — DDMin on Grover + MQT algorithms =="
confirm "Run Exp 1 (${RUNS} runs per layout/algorithm, stops at ${EXP1_BUDGET_MIN} min total QPU)?" || exit 0
python -m scripts.xalg.ddmin "${COMMON[@]}" --runs "$RUNS" --parallel "$PARALLEL" --budget-min "$EXP1_BUDGET_MIN"
echo "(Exp 1 exit code $?; 2 = stopped by budget)"

echo; echo "== Step 4: Exp 2 — plan variants (no QPU) =="
python -m scripts.xalg.variants "${COMMON[@]}" --plan --budget-min "$BUDGET_MIN"

echo; echo "== Step 5: Exp 2 — run variants =="
if confirm "Run the planned variant sets on $BACKEND?"; then
  python -m scripts.xalg.variants "${COMMON[@]}" --run --budget-min "$BUDGET_MIN"
fi
