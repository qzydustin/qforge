#!/usr/bin/env python3
"""
Step 1 — compile all candidate algorithms and run a SIMULATOR-ONLY preflight.

Uses NO QPU time.  With --hardware ibm it connects only to read the backend's
target and latest calibration (for the noise model) and queue length.

For every (layout, algorithm):
  * compile at O3 onto the fixed layout with a fixed transpiler seed,
  * measure native-gate count, cz count, depth, number of 3-moment segments,
  * ideal output's TVD from uniform (the oracle needs a non-uniform output),
  * model error TVD(ideal, noisy) vs. shot-noise floor 2*TVD(noisy1, noisy2),
and mark the circuit usable only if all of:
    segments >= 8,  TVD(ideal, uniform) >= 0.15,  TVD(ideal, noisy) >= 1.5 * floor.

Algorithms with (near-)uniform outputs (QFT, graph state) cannot separate
hardware from model, so they fail the TVD-from-uniform check.

Usage:
    python -m scripts.xalg.prepare --backend ibm_fez
    python -m scripts.xalg.prepare --backend ibm_fez --hardware emulate   # offline
"""

from __future__ import annotations

import argparse

from scripts.xalg.common import (
    GROVER, MIN_MODEL_OVER_FLOOR, MIN_SEGMENTS, MIN_TVD_FROM_UNIFORM, MOMENTS_PER_SEGMENT,
    MQT_ALGORITHMS, SEED_TRANSPILER, add_common_args, build_logical, circuit_path, make_executor,
    now, parse_layouts, preflight_path, results_root, save_qpy, software_versions,
)
from qrisk.circuits import compile_isa
from qrisk.ddmin import save_report
from qrisk.metrics import calculate_tvd
from qrisk.partition import segment_circuit


def tvd_from_uniform(counts: dict, n_bits: int) -> float:
    total = sum(counts.values())
    k = 2 ** n_bits
    seen = sum(abs(c / total - 1 / k) for c in counts.values())
    unseen = (k - len(counts)) / k
    return 0.5 * (seen + unseen)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(p)
    p.add_argument("--algorithms", nargs="*", default=[GROVER] + MQT_ALGORITHMS)
    args = p.parse_args()

    root = results_root(args)
    layouts = parse_layouts(args.layouts, args.backend)
    ex = make_executor(args)  # no budget needed: simulators only
    shots = ex.config["execution"]["shots"]

    if args.hardware == "ibm":
        try:
            st = ex.backend.status()
            print(f"{args.backend}: operational={st.operational}, pending_jobs={st.pending_jobs}")
        except Exception:
            pass
    print(f"Calibration snapshot: {ex.calibration_info()}")

    rows = []
    hdr = f"{'layout':>18} {'algorithm':>15} {'ops':>5} {'cz':>4} {'segs':>5} {'dUnif':>6} {'dModel':>7} {'floor':>6}  result"
    print(hdr)
    print("-" * len(hdr))
    for layout in layouts:
        for alg in args.algorithms:
            row = {"layout": layout, "algorithm": alg, "passed": False}
            try:
                isa = compile_isa(build_logical(alg), ex.backend, layout, seed_transpiler=SEED_TRANSPILER)
            except Exception as e:
                row["reason"] = f"build/compile error: {e}"
                rows.append(row)
                print(f"{str(layout):>18} {alg:>15}  ERROR {e}")
                continue
            ops = {k: v for k, v in isa.count_ops().items() if k not in ("measure", "barrier")}
            n_bits = isa.num_clbits
            segs = len(segment_circuit(isa, MOMENTS_PER_SEGMENT))
            ideal = ex.run_circuit(isa, "ideal_simulator", shots)["counts"]
            noisy1 = ex.run_circuit(isa, "noisy_simulator", shots)["counts"]
            noisy2 = ex.run_circuit(isa, "noisy_simulator", shots)["counts"]
            d_unif = tvd_from_uniform(ideal, n_bits)
            d_model, _ = calculate_tvd(ideal, noisy1)
            floor = 2 * calculate_tvd(noisy1, noisy2)[0]

            reasons = []
            if segs < MIN_SEGMENTS:
                reasons.append(f"only {segs} segments (<{MIN_SEGMENTS})")
            if d_unif < MIN_TVD_FROM_UNIFORM:
                reasons.append(f"near-uniform output (TVD from uniform {d_unif:.2f} < {MIN_TVD_FROM_UNIFORM})")
            if d_model < MIN_MODEL_OVER_FLOOR * floor:
                reasons.append(f"model error {d_model:.3f} < {MIN_MODEL_OVER_FLOOR}x shot-noise floor {floor:.3f}")
            row.update({
                "passed": not reasons,
                "reason": "; ".join(reasons) or "ok",
                "native_ops": sum(ops.values()),
                "cz": ops.get("cz", 0),
                "depth": isa.depth(),
                "segments": segs,
                "measured_bits": n_bits,
                "tvd_ideal_uniform": round(d_unif, 4),
                "tvd_ideal_noisy": round(d_model, 4),
                "shot_noise_floor": round(floor, 4),
                "qpy": str(circuit_path(root, args.backend, layout, alg).relative_to(root)),
            })
            save_qpy(isa, circuit_path(root, args.backend, layout, alg))
            rows.append(row)
            print(f"{str(layout):>18} {alg:>15} {row['native_ops']:>5} {row['cz']:>4} {segs:>5} "
                  f"{d_unif:>6.2f} {d_model:>7.3f} {floor:>6.3f}  "
                  f"{'PASS' if row['passed'] else 'fail: ' + row['reason']}")

    out = {
        "created": now(),
        "backend": args.backend,
        "hardware": args.hardware,
        "shots": shots,
        "seed_transpiler": SEED_TRANSPILER,
        "thresholds": {
            "min_segments": MIN_SEGMENTS,
            "min_tvd_from_uniform": MIN_TVD_FROM_UNIFORM,
            "min_model_over_floor": MIN_MODEL_OVER_FLOOR,
        },
        "calibration": ex.calibration_info(),
        "versions": software_versions(),
        "rows": rows,
    }
    save_report(out, preflight_path(root, args.backend))
    n_pass = sum(r["passed"] for r in rows)
    print(f"\n{n_pass}/{len(rows)} circuits usable. Preflight: {preflight_path(root, args.backend)}")


if __name__ == "__main__":
    main()
