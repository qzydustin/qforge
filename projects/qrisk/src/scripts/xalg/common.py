"""
Shared settings and helpers for the cross-algorithm experiments in scripts/xalg/.

Question: are the abnormal gate patterns that QRisk isolates from Grover
specific to Grover, or do other algorithms compiled onto the same physical
qubits expose the same patterns?

  Exp 1 (ddmin.py):    DDMin on Grover + MQT Bench algorithms, same
                       layouts, same calibration window.
  Exp 2 (variants.py): dose-response of Grover's pattern inside other
                       algorithms (commuting-swap variants, 0..k hits).

Outputs go to RESULTS_DIR/xalg (hardware) or RESULTS_DIR/xalg_dryrun
(emulated), or to --results-dir.
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

warnings.filterwarnings("ignore", category=DeprecationWarning)

from qiskit import QuantumCircuit, qpy  # noqa: E402

from qrisk.budget import QPUBudget  # noqa: E402
from qrisk.circuits import grover_3q, layout_str  # noqa: E402
from qrisk.config import load_config  # noqa: E402
from qrisk.executor import QuantumExecutor  # noqa: E402
from qrisk.paths import CONFIG_FILE, RESULTS_DIR  # noqa: E402

# Two layouts per backend: the paper's headline layout plus the layout with
# the most recent validated post-update pattern.
DEFAULT_LAYOUTS: Dict[str, List[List[int]]] = {
    "ibm_fez": [[46, 47, 48, 57], [97, 106, 107, 108]],
    "ibm_marrakesh": [[6, 7, 8, 17], [118, 128, 129, 130]],
    "ibm_kingston": [[138, 150, 151, 152], [126, 127, 128, 137]],
}

GROVER = "qrisk_grover3x"  # the paper's discovery workload (3x repeated Grover-3 + ancilla)

# 4-qubit MQT Bench algorithms considered.  Preflight decides which are usable.
MQT_ALGORITHMS = [
    "ae", "qpeinexact", "qwalk", "randomcircuit",   # default Exp 1 set
    "wstate", "ghz", "qpeexact", "dj", "bv", "grover",
    "qft", "graphstate", "qftentangled",           # expected to FAIL preflight
]
DEFAULT_EXP1 = [GROVER, "ae", "qpeinexact", "qwalk", "randomcircuit"]

# Preflight thresholds (see prepare.py).
MIN_SEGMENTS = 8
MIN_TVD_FROM_UNIFORM = 0.15  # the paper's own Grover-3x reference sits at ~0.20
MIN_MODEL_OVER_FLOOR = 1.5

SEED_TRANSPILER = 7
MOMENTS_PER_SEGMENT = 3


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

def parse_layouts(text: Optional[str], backend: str) -> List[List[int]]:
    """'46,47,48,57;97,106,107,108' -> [[46,47,48,57],[97,106,107,108]]"""
    if not text:
        return DEFAULT_LAYOUTS[backend]
    return [[int(x) for x in part.split(",")] for part in text.split(";") if part.strip()]


def results_root(args) -> Path:
    if getattr(args, "results_dir", None):
        return Path(args.results_dir)
    sub = "xalg_dryrun" if args.hardware == "emulate" else "xalg"
    return RESULTS_DIR / sub


def circuit_path(root: Path, backend: str, layout: List[int], alg: str) -> Path:
    return root / "circuits" / backend / layout_str(layout) / f"{alg}.qpy"


def preflight_path(root: Path, backend: str) -> Path:
    return root / "circuits" / backend / "preflight.json"


def save_qpy(circuit: QuantumCircuit, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        qpy.dump([circuit], f)


def load_qpy(path: Path) -> QuantumCircuit:
    with open(path, "rb") as f:
        return list(qpy.load(f))[0]


def read_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_preflight(root: Path, backend: str) -> Dict[str, Any]:
    path = preflight_path(root, backend)
    if not path.exists():
        sys.exit(f"No preflight found at {path}. Run prepare.py first.")
    return read_json(path)


def passing_algorithms(preflight: Dict[str, Any], layout: List[int]) -> List[str]:
    return [r["algorithm"] for r in preflight["rows"]
            if r["layout"] == layout and r["passed"]]


# ---------------------------------------------------------------------------
# Circuits
# ---------------------------------------------------------------------------

def build_logical(alg: str) -> QuantumCircuit:
    if alg == GROVER:
        return grover_3q(iterations=3)
    from mqt.bench import BenchmarkLevel, get_benchmark
    qc = get_benchmark(alg, BenchmarkLevel.ALG, 4)
    if qc.num_qubits != 4:
        raise ValueError(f"{alg} produced {qc.num_qubits} qubits, expected 4")
    return qc


# ---------------------------------------------------------------------------
# CLI / executor
# ---------------------------------------------------------------------------

def add_common_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--backend", default="ibm_fez",
                   choices=sorted(DEFAULT_LAYOUTS), help="IBM backend")
    p.add_argument("--layouts", default=None,
                   help="Semicolon-separated layouts, e.g. '46,47,48,57;97,106,107,108' "
                        "(default: two layouts per backend)")
    p.add_argument("--config", default=str(CONFIG_FILE),
                   help="IBM Quantum config with the account tokens (default: %(default)s); "
                        "not read with --hardware emulate")
    p.add_argument("--hardware", default="ibm", choices=["ibm", "emulate"],
                   help="'emulate' = offline dry run: fake backend + planted fault, no IBM calls")
    p.add_argument("--results-dir", default=None,
                   help=f"Default: {RESULTS_DIR}/xalg (ibm) or {RESULTS_DIR}/xalg_dryrun (emulate)")
    p.add_argument("--budget-min", type=float, default=40.0,
                   help="Hard cap on total QPU minutes across ALL xalg scripts (ledger-based)")


def make_budget(args) -> QPUBudget:
    return QPUBudget(results_root(args) / "qpu_ledger.jsonl", cap_seconds=args.budget_min * 60.0)


def make_executor(args, budget: Optional[QPUBudget] = None, emulate_fault=None) -> QuantumExecutor:
    try:
        # Offline dry runs never touch IBM, so they never read the credentials file.
        cfg = load_config(args.config, backend=args.backend, example=args.hardware == "emulate")
    except (FileNotFoundError, ValueError) as e:
        sys.exit(str(e))
    cfg.setdefault("execution", {}).setdefault("delta_debug", {})["moments_per_segment"] = MOMENTS_PER_SEGMENT
    cfg["execution"].setdefault("shots", 8192)
    return QuantumExecutor(
        config=cfg,
        backend_name=args.backend,
        refresh_each_job=False,
        budget=budget,
        hardware=args.hardware,
        emulate_fault=emulate_fault,
    )


def default_emulate_fault(reference: QuantumCircuit) -> Dict[str, Any]:
    """Dry-run 'hardware' = noise model + extra 8% depolarizing on the most
    used cz pair of the reference (Grover) circuit."""
    from collections import Counter
    pairs = Counter(
        tuple(sorted(reference.find_bit(q).index for q in inst.qubits))
        for inst in reference.data if inst.operation.name == "cz"
    )
    pair = list(pairs.most_common(1)[0][0])
    return {"gate": "cz", "qubits": pair, "p": 0.08}


def software_versions() -> Dict[str, str]:
    import importlib.metadata as md
    out = {}
    for pkg in ("qiskit", "qiskit-aer", "qiskit-ibm-runtime", "mqt.bench"):
        try:
            out[pkg] = md.version(pkg)
        except Exception:
            out[pkg] = "unknown"
    return out


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")
