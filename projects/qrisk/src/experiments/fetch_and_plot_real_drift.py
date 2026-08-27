#!/usr/bin/env python3
"""
Fetch real historical calibration data from IBM backends and plot drift.

Uses backend.properties(datetime=...) to retrieve historical calibration snapshots.

Usage:
    python experiments/fetch_and_plot_real_drift.py \
        --backends ibm_fez ibm_marrakesh \
        --qubits-fez 24 25 \
        --qubits-marrakesh 6 7 \
        --start-date 2026-02-01 \
        --end-date 2026-06-30
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Import the IBM connector if available
try:
    sys.path.insert(0, str(REPO_ROOT.parent / "qrisk-paper" / "6a20559882028ed723a87bd8"))
    from ibm_quantum_connector import QuantumServiceManager
    HAS_CONNECTOR = True
except ImportError:
    HAS_CONNECTOR = False
    print("Warning: ibm_quantum_connector not found, falling back to qiskit_ibm_runtime")

BACKEND_COLORS = ["#0072B2", "#D55E00", "#009E73", "#CC79A7"]


def fetch_historical_properties(backend, timestamps):
    """
    Fetch backend properties for a list of historical timestamps.

    Returns list of (timestamp, properties) tuples.
    """
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


def extract_gate_error(properties, qubit, gate_type='sx'):
    """Extract gate error rate for a specific qubit."""
    try:
        return properties.gate_error(gate_type, [qubit])
    except Exception:
        return None


def fetch_real_data(backend_specs, start_date, end_date, sample_interval_days=7):
    """
    Fetch real calibration data for multiple backends.

    Args:
        backend_specs: [(backend_name, [qubits]), ...]
        start_date: datetime
        end_date: datetime
        sample_interval_days: How often to sample (default: weekly)

    Returns:
        (timestamps, series) where series is list of dicts with backend/qubit/errors
    """
    # Generate sampling timestamps
    timestamps = []
    current = start_date
    while current <= end_date:
        timestamps.append(current)
        current += timedelta(days=sample_interval_days)

    print(f"Fetching {len(timestamps)} time points from {start_date.date()} to {end_date.date()}")

    # Load IBM credentials
    config_path = REPO_ROOT / "quantum_config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    with open(config_path) as f:
        config = json.load(f)

    accounts = config.get("ibm_quantum", {}).get("accounts", [])
    if not accounts:
        raise ValueError("No IBM accounts in config")

    account = accounts[0]

    # Initialize service
    if HAS_CONNECTOR:
        mgr = QuantumServiceManager(config_path)
        service = mgr.get_service(account["name"])
    else:
        from qiskit_ibm_runtime import QiskitRuntimeService
        service = QiskitRuntimeService(
            channel="ibm_quantum_platform",
            token=account["token"],
            instance=account.get("instance", "ibm-q/open/main")
        )

    # Fetch data for each backend
    all_series = []

    for b_idx, (backend_name, qubits) in enumerate(backend_specs):
        print(f"\nBackend: {backend_name}")
        backend = service.backend(backend_name)

        # Fetch historical properties
        props_history = fetch_historical_properties(backend, timestamps)

        if not props_history:
            print(f"  No data retrieved for {backend_name}")
            continue

        # Extract error rates for each qubit
        base_color = BACKEND_COLORS[b_idx % len(BACKEND_COLORS)]

        for q_idx, qubit in enumerate(qubits):
            errors = []
            valid_timestamps = []

            for ts, props in props_history:
                error = extract_gate_error(props, qubit, 'sx')
                if error is not None:
                    errors.append(error)
                    valid_timestamps.append(ts)

            if errors:
                alpha = 1.0 if q_idx == 0 else 0.65
                all_series.append({
                    "backend": backend_name,
                    "qubit": qubit,
                    "color": base_color,
                    "alpha": alpha,
                    "timestamps": valid_timestamps,
                    "errors": np.array(errors),
                })
                print(f"  Q{qubit}: {len(errors)} data points")

    return all_series


def plot_real_drift(series, output_path):
    """Plot real calibration drift data."""
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
            label=f"{s['backend'].replace('ibm_', '')} Q{s['qubit']}",
        )

    ax.set_xlabel("Date")
    ax.set_ylabel("SX gate error rate (\\%)")
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
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"\n✓ Saved {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Fetch and plot real IBM calibration drift")
    parser.add_argument("--backends", nargs="+", default=["ibm_fez", "ibm_marrakesh"],
                       help="Backend names")
    parser.add_argument("--qubits-fez", nargs="+", type=int, default=[24, 25],
                       help="Qubits for ibm_fez")
    parser.add_argument("--qubits-marrakesh", nargs="+", type=int, default=[6, 7],
                       help="Qubits for ibm_marrakesh")
    parser.add_argument("--start-date", default="2026-02-01",
                       help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", default="2026-06-30",
                       help="End date (YYYY-MM-DD)")
    parser.add_argument("--interval", type=int, default=7,
                       help="Sampling interval in days (default: 7)")
    parser.add_argument("--output", default=None,
                       help="Output path (default: figures/calibration_drift.pdf)")

    args = parser.parse_args()

    # Parse dates
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    # Build backend specs
    backend_specs = []
    if "ibm_fez" in args.backends:
        backend_specs.append(("ibm_fez", args.qubits_fez))
    if "ibm_marrakesh" in args.backends:
        backend_specs.append(("ibm_marrakesh", args.qubits_marrakesh))

    if not backend_specs:
        print("Error: No valid backends specified")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_dir = REPO_ROOT.parent / "qrisk-paper" / "6a20559882028ed723a87bd8" / "figures"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "calibration_drift.pdf"

    # Fetch and plot
    series = fetch_real_data(backend_specs, start_date, end_date, args.interval)

    if not series:
        print("Error: No data fetched")
        sys.exit(1)

    plot_real_drift(series, output_path)


if __name__ == "__main__":
    main()

    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"\n✓ Saved {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Fetch and plot real IBM calibration drift")
    parser.add_argument("--backends", nargs="+", default=["ibm_fez", "ibm_marrakesh"])
    parser.add_argument("--qubits-fez", nargs="+", type=int, default=[24, 25])
    parser.add_argument("--qubits-marrakesh", nargs="+", type=int, default=[6, 7])
    parser.add_argument("--start-date", default="2026-02-01", help="YYYY-MM-DD")
    parser.add_argument("--end-date", default="2026-06-30", help="YYYY-MM-DD")
    parser.add_argument("--interval-days", type=int, default=7, help="Sampling interval in days")
    parser.add_argument("--output", default=None)

    args = parser.parse_args()

    # Parse dates
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    # Build backend specs
    backend_specs = []
    if "ibm_fez" in args.backends:
        backend_specs.append(("ibm_fez", args.qubits_fez))
    if "ibm_marrakesh" in args.backends:
        backend_specs.append(("ibm_marrakesh", args.qubits_marrakesh))

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_dir = REPO_ROOT.parent / "qrisk-paper" / "6a20559882028ed723a87bd8" / "figures"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "calibration_drift.pdf"

    # Fetch real data
    series = fetch_real_data(backend_specs, start_date, end_date, args.interval_days)

    if not series:
        print("Error: No data fetched")
        sys.exit(1)

    # Plot
    plot_real_drift(series, output_path)


if __name__ == "__main__":
    main()
