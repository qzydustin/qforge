#!/usr/bin/env python3
"""
Fetch historical calibration snapshots of IBM backends and plot one gate's
error rate over time, one line per qubit (the paper's calibration-drift figure).

Each sampled date is one backend.properties(datetime=...) call; no QPU time is used.

Usage:
    python -m scripts.calibration.fetch_calibration_drift \\
        --backends ibm_fez ibm_marrakesh --qubits 24,25 6,7 \\
        --start-date 2026-02-01 --end-date 2026-06-30

    python -m scripts.calibration.fetch_calibration_drift \\
        --backends ibm_fez --qubits 24-25 --gate cz --output cz_drift.pdf
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

from qrisk.config import load_config
from qrisk.ibm_runtime import QuantumServiceManager
from qrisk.paths import DERIVED_DIR

BACKEND_COLORS = ["#0072B2", "#D55E00", "#009E73", "#CC79A7"]


def parse_qubits(spec: str) -> list[tuple[int, ...]]:
    """'24,25' -> [(24,), (25,)];  '24-25' -> [(24, 25)] (a pair, for two-qubit gates)."""
    return [tuple(int(q) for q in item.split("-")) for item in spec.split(",")]


def fetch_historical_properties(backend, timestamps):
    """[(timestamp, properties)] for every timestamp that has a snapshot."""
    results = []
    for ts in timestamps:
        try:
            props = backend.properties(datetime=ts)
            if props:
                results.append((ts, props))
                print(f"  ✓ {ts.date()}")
            else:
                print(f"  ✗ {ts.date()} (no data)")
        except Exception as e:
            print(f"  ✗ {ts.date()} ({e})")
    return results


def gate_error(properties, gate, qubits):
    try:
        return properties.gate_error(gate, list(qubits))
    except Exception:
        return None


def fetch_real_data(service, backend_specs, timestamps, gate):
    """One series per (backend, qubits); backend_specs is [(backend_name, [qubits, ...]), ...]."""
    all_series = []
    for b_idx, (backend_name, qubit_sets) in enumerate(backend_specs):
        print(f"\nBackend: {backend_name}")
        props_history = fetch_historical_properties(service.backend(backend_name), timestamps)
        if not props_history:
            print(f"  No data retrieved for {backend_name}")
            continue

        for q_idx, qubits in enumerate(qubit_sets):
            points = [(ts, gate_error(props, gate, qubits)) for ts, props in props_history]
            points = [(ts, err) for ts, err in points if err is not None]
            name = "Q" + "-".join(map(str, qubits))
            if points:
                all_series.append({
                    "label": f"{backend_name.replace('ibm_', '')} {name}",
                    "color": BACKEND_COLORS[b_idx % len(BACKEND_COLORS)],
                    "alpha": 1.0 if q_idx == 0 else 0.65,
                    "timestamps": [ts for ts, _ in points],
                    "errors": np.array([err for _, err in points]),
                })
                print(f"  {name}: {len(points)} data points")
    return all_series


def plot_real_drift(series, gate, output_path: Path):
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.linewidth": 0.6,
        "axes.edgecolor": "#444444",
    })

    fig, ax = plt.subplots(figsize=(7.0, 2.5))

    for s in series:
        ax.plot(
            s["timestamps"], s["errors"] * 100,
            color=s["color"], linestyle="-", linewidth=1.3, alpha=s["alpha"],
            marker="o", markersize=3,
            label=s["label"],
        )

    ax.set_xlabel("Date")
    ax.set_ylabel(f"{gate.upper()} gate error rate (%)")
    ax.grid(True, alpha=0.25, linewidth=0.5)
    ax.tick_params(labelsize=8)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    for label in ax.get_xticklabels():
        label.set_rotation(0)

    ax.legend(
        loc="upper left", frameon=False, fontsize=7.5,
        ncol=2, columnspacing=1.0, handlelength=1.8,
    )

    fig.tight_layout(pad=0.4)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"\n✓ Saved {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--backends", nargs="+", default=["ibm_fez", "ibm_marrakesh"])
    parser.add_argument("--qubits", nargs="+", default=["24,25", "6,7"],
                        help="one comma-separated list per backend, in --backends order; "
                             "write a pair as a-b for a two-qubit --gate (default: 24,25 6,7)")
    parser.add_argument("--gate", default="sx", help="gate whose error rate is plotted (default: sx)")
    parser.add_argument("--start-date", default="2026-02-01", help="YYYY-MM-DD")
    parser.add_argument("--end-date", default="2026-06-30", help="YYYY-MM-DD")
    parser.add_argument("--interval", type=int, default=7, help="sampling interval in days (default: 7)")
    parser.add_argument("--output", type=Path, default=DERIVED_DIR / "figures" / "calibration_drift.pdf",
                        help="default: <data>/derived/figures/calibration_drift.pdf")
    args = parser.parse_args()

    if len(args.qubits) != len(args.backends):
        parser.error(f"--qubits needs one list per backend ({len(args.backends)}), got {len(args.qubits)}")
    backend_specs = [(b, parse_qubits(q)) for b, q in zip(args.backends, args.qubits)]

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    timestamps = []
    current = start_date
    while current <= end_date:
        timestamps.append(current)
        current += timedelta(days=args.interval)
    print(f"Fetching {len(timestamps)} time points from {start_date.date()} to {end_date.date()}")

    manager = QuantumServiceManager(load_config())
    if not manager.connect():
        sys.exit("Error: could not connect to IBM Quantum")

    series = fetch_real_data(manager.service, backend_specs, timestamps, args.gate)
    if not series:
        sys.exit("Error: No data fetched")

    plot_real_drift(series, args.gate, args.output)


if __name__ == "__main__":
    main()
