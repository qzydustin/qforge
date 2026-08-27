> **Vendored snapshot.** Source: https://github.com/qzydustin/qrisk @ `0d60343` (fetched 2026-08-27).
> Code lives in [`src/`](src/). Experiment outputs (`artifacts/`) were removed to keep this
> platform repo lightweight — fetch the upstream repository for the full artifact set.

# QRisk

QRisk is a research prototype for isolating recurring, execution-dependent
hardware--model discrepancies in quantum circuits. It combines moment-level
delta debugging with a stochastic discrepancy oracle and cross-window
recurrence analysis.

## What is included

- `quantum/`: core library for circuit partitioning, DDMin, execution, metrics,
  pattern storage, and pattern-disruption rewrites.
- `experiments/`: reproducible drivers for circuit generation, DDMin runs,
  variant generation, verification, ablation, and calibration-drift plots.
- `analysis/`: scripts that construct the analysis tables, recurrence summaries,
  minimality checks, sensitivity analyses, and RQ3 statistics/plots.
- `artifacts/`: public QPY circuit inputs and DDMin reports used by the study.
  Local configuration snapshots and hardware job identifiers have been removed.
- `tests/`: unit tests for moment partitioning and DDMin ablations.

No credentials, raw hardware job records, virtual environments, local logs, or
private Git history are included.

## Installation

QRisk requires Python 3.10 or later.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure IBM Quantum access

Hardware execution is optional. Unit tests and data inspection do not require
an IBM Quantum account.

To execute on hardware, create a local configuration file from the template:

```bash
cp quantum_config.example.json quantum_config.json
```

Set a valid IBM Quantum token in `quantum_config.json`. This file is ignored by
Git and must never be committed. Prefer a dedicated, least-privilege token for
each local environment; revoke it immediately if it is disclosed.

## Quick checks

Run the offline tests:

```bash
pytest -q
```

Run DDMin with a prepared circuit directory:

```bash
python -m quantum.cli --algorithm path/to/circuit_directory --config quantum_config.json
```

Generate and run the Grover-3 discovery workload on a configured backend:

```bash
python experiments/generate_and_run_grover3.py --backend ibm_fez
```

These commands submit jobs when `--test-mode` is not used. Review your IBM
Quantum account limits before running them.
