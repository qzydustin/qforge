> **Vendored snapshot.** Source: https://github.com/qzydustin/qrisk @ `cdd348f` (fetched 2026-10-15). Code lives in [`src/`](src/). The hardware data (`data/`, 54 MB) and the test that reads it were left out to keep this platform repo lightweight — fetch the upstream repository for them.

# QRisk

QRisk partitions a compiled quantum circuit into moment-based segments and runs DDMin with the oracle **R = TVD(ideal, real) / TVD(ideal, noisy)** to isolate the segments where real hardware is worse than the noise model predicts (R > 1 + τ, τ calibrated from shot noise). Patterns that are rediscovered across calibration windows are stored and broken by commuting gate swaps.

## Layout (`src/`)

| Path | Contents |
|---|---|
| `qrisk/` | The library: moment segmentation (`partition.py`), DDMin (`ddmin.py`), circuit execution on simulators, IBM hardware or an offline emulation (`executor.py`, `ibm_runtime.py`), gate tokens and pattern keys (`tokens.py`), qubit-timeline matching and commuting swaps (`patterns.py`), the Grover-3 workload (`circuits.py`), QPU budget ledger (`budget.py`), TVD and Hellinger (`metrics.py`), config loading (`config.py`), data layout (`paths.py`). `python -m qrisk.cli` runs DDMin on one group. |
| `scripts/grover/` | Compile Grover-3 for every (backend, layout) group and run DDMin on IBM hardware. |
| `scripts/verify/` | Verify sets: commuting-swap variants of a group's circuit binned by pattern hits, bucket top-up, hardware runs. |
| `scripts/xalg/` | Cross-algorithm experiments: compile Grover + MQT Bench workloads on the same qubits, run DDMin on each under a QPU budget, build dose-response variants. |
| `scripts/calibration/` | Historical calibration snapshots of a gate's error rate and the drift plot. |
| `scripts/ibm_accounts.py` | Remaining quota per IBM account; cancel pending jobs. |
| `scripts/smoke_test.py` | Executor smoke test on a Bell circuit (offline unless `--real`). |
| `config/` | `quantum_config.example.json`; copy it to `config/quantum_config.json` and add your IBM account. |
| `tests/` | Unit tests; they run offline. |

## Setup

```bash
cd src
python -m venv .venv && .venv/bin/pip install -r requirements.txt
source .venv/bin/activate
python -m pytest
```

Every command runs from `src/` as a module (`python -m ...`), which is what puts `qrisk` and `scripts` on the import path. The drivers read and write `src/data/`; clone the upstream repository to get the paper's runs there.

## Run

```bash
python -m qrisk.cli --algorithm <group> --test-mode
```

runs DDMin on `data/artifacts/<group>` with the noisy simulator standing in for the device. It connects to IBM Quantum (`config/quantum_config.json`) for the backend and its noise model, and writes the report JSON into the group directory. Without `--test-mode` the oracle runs on the device.

- Discovery: `python -m scripts.grover.generate_and_run_grover3` compiles the Grover-3 groups and runs DDMin on each.
- Verify sets: `python -m scripts.verify.generate_verify_variants --group <group> --auto-pattern` builds the hit-count buckets; `python -m scripts.verify.run_verify_batch --verify-dir <group>/variants/verify` runs them on hardware.
- Cross-algorithm experiments: `RESULTS_DIR=<dir> HARDWARE=emulate RUNS=1 bash scripts/xalg/run_all.sh ibm_fez` is the offline dry run; without `HARDWARE=emulate` it runs on the device under a 40-minute QPU cap.
- Calibration drift: `python -m scripts.calibration.fetch_calibration_drift`.
