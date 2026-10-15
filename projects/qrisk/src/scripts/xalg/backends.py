#!/usr/bin/env python3
"""
Step 0 — check the IBM account: remaining quota, and which of the study's
backends are online and how long their queues are.  Uses NO QPU time.

Usage:
    python -m scripts.xalg.backends
"""

from __future__ import annotations

import argparse

from scripts.xalg.common import DEFAULT_LAYOUTS
from qrisk.config import load_config
from qrisk.ibm_runtime import QuantumServiceManager
from qrisk.paths import CONFIG_FILE


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", default=str(CONFIG_FILE))
    args = p.parse_args()

    mgr = QuantumServiceManager(load_config(args.config))
    if not mgr.connect():
        raise SystemExit(f"Could not connect — check token/instance in {args.config}")
    svc = mgr.service
    try:
        usage = svc.usage()
        rem = usage.get("usage_remaining_seconds")
        if rem is not None:
            print(f"Instance quota remaining: {rem:.0f} s ({rem / 60:.1f} min)")
        else:
            print(f"Usage info: {usage}")
    except Exception as e:
        print(f"(usage not available: {e})")

    available = {b.name for b in svc.backends()}
    print(f"\n{'backend':>15} {'online':>7} {'queue':>6}")
    for name in DEFAULT_LAYOUTS:
        if name not in available:
            print(f"{name:>15}  not available on this instance")
            continue
        st = svc.backend(name).status()
        print(f"{name:>15} {str(st.operational):>7} {st.pending_jobs:>6}")
    others = sorted(available - set(DEFAULT_LAYOUTS))
    if others:
        print(f"\nOther backends on this instance: {', '.join(others)}")
    print("\nPick the study backend with the shortest queue (ibm_fez or ibm_marrakesh preferred: "
          "they have the paper's validated patterns).")


if __name__ == "__main__":
    main()
