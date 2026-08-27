#!/usr/bin/env python3
"""
Plot gate error rate changes over time for specific qubits on IBM backends.

Usage:
    python experiments/plot_gate_error_drift.py --backend ibm_fez --qubits 0 1
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from qiskit_ibm_runtime import QiskitRuntimeService


def get_calibration_history(backend_name, start_date, end_date, account_config):
    """
    Fetch calibration history for a backend.

    Args:
        backend_name: Name of the IBM backend
        start_date: Start datetime
        end_date: End datetime
        account_config: Account configuration dict

    Returns:
        List of (datetime, properties_dict) tuples
    """
    service = QiskitRuntimeService(
        channel="ibm_quantum",
        token=account_config["token"],
        instance=account_config.get("instance", "ibm-q/open/main")
    )

    backend = service.backend(backend_name)

    # Get calibration data at different time points
    calibration_data = []

    # Try to get historical data
    # Note: IBM API might have limitations on historical data access
    try:
        properties = backend.properties()
        if properties:
            calibration_data.append((datetime.now(), properties))
    except Exception as e:
        print(f"Warning: Could not fetch current properties: {e}", file=sys.stderr)

    return calibration_data


def extract_gate_errors(properties, qubit_pairs):
    """
    Extract gate error rates for specific qubit pairs.

    Args:
        properties: Backend properties object
        qubit_pairs: List of (q1, q2) tuples or single qubits

    Returns:
        dict mapping (q1, q2) or q to error rate
    """
    errors = {}

    for item in qubit_pairs:
        if isinstance(item, tuple):
            # Two-qubit gate
            q1, q2 = item
            try:
                # Get CX gate error for this pair
                gate_error = properties.gate_error('cx', [q1, q2])
                errors[(q1, q2)] = gate_error
            except Exception as e:
                print(f"Warning: Could not get CX error for qubits {q1}, {q2}: {e}", file=sys.stderr)
        else:
            # Single-qubit gate
            q = item
            try:
                # Get single-qubit gate error (e.g., sx)
                gate_error = properties.gate_error('sx', [q])
                errors[q] = gate_error
            except Exception as e:
                print(f"Warning: Could not get SX error for qubit {q}: {e}", file=sys.stderr)

    return errors


def plot_error_drift(calibration_history, qubit_pairs, output_path):
    """
    Plot gate error rate changes over time.

    Args:
        calibration_history: List of (datetime, properties) tuples
        qubit_pairs: List of qubit specifications
        output_path: Path to save the plot
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Extract time series for each qubit pair
    for item in qubit_pairs:
        times = []
        errors = []

        for timestamp, properties in calibration_history:
            error_dict = extract_gate_errors(properties, [item])
            if item in error_dict:
                times.append(timestamp)
                errors.append(error_dict[item] * 100)  # Convert to percentage

        if times:
            label = f"CX({item[0]},{item[1]})" if isinstance(item, tuple) else f"SX({item})"
            ax.plot(times, errors, marker='o', label=label, linewidth=2)

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Gate Error Rate (%)', fontsize=12)
    ax.set_title('IBM Backend Gate Error Rate Drift Over Time', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate()

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Plot gate error drift over time")
    parser.add_argument("--backend", required=True, help="IBM backend name (e.g., ibm_fez)")
    parser.add_argument("--qubits", nargs='+', type=int, help="Qubit indices (e.g., 0 1 for qubits 0 and 1)")
    parser.add_argument("--pairs", nargs='+', help="Qubit pairs (e.g., '0,1' '1,2')")
    parser.add_argument("--days", type=int, default=30, help="Number of days of history to fetch")
    parser.add_argument("--output", default="gate_error_drift.pdf", help="Output file path")
    parser.add_argument("--config", default=REPO_ROOT / "quantum_config.json", help="Config file path")

    args = parser.parse_args()

    # Load config
    with open(args.config) as f:
        config = json.load(f)

    # Get first account
    accounts = config.get("ibm_quantum", {}).get("accounts", [])
    if not accounts:
        print("Error: No IBM accounts found in config", file=sys.stderr)
        sys.exit(1)

    account = accounts[0]

    # Prepare qubit specifications
    qubit_specs = []
    if args.qubits:
        qubit_specs.extend(args.qubits)
    if args.pairs:
        for pair_str in args.pairs:
            q1, q2 = map(int, pair_str.split(','))
            qubit_specs.append((q1, q2))

    if not qubit_specs:
        print("Error: Must specify --qubits or --pairs", file=sys.stderr)
        sys.exit(1)

    # Fetch calibration history
    end_date = datetime.now()
    start_date = end_date - timedelta(days=args.days)

    print(f"Fetching calibration data for {args.backend}...")
    print(f"Time range: {start_date.date()} to {end_date.date()}")
    print(f"Qubits/pairs: {qubit_specs}")

    calibration_history = get_calibration_history(args.backend, start_date, end_date, account)

    if not calibration_history:
        print("Warning: No calibration data retrieved", file=sys.stderr)
        sys.exit(1)

    print(f"Retrieved {len(calibration_history)} calibration snapshots")

    # Plot
    plot_error_drift(calibration_history, qubit_specs, args.output)


if __name__ == "__main__":
    main()
