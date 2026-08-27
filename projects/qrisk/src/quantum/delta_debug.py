from __future__ import annotations

from typing import List, Dict, Any, Optional, Sequence
from datetime import datetime
import json

from qiskit import QuantumCircuit
from .metrics import calculate_tvd
from .partition import segment_circuit


class QuantumDeltaDebugger:
    """Quantum Circuit Delta Debugger (DDMin-based).

    Identifies minimal sets of circuit segments responsible for the gap
    between a noise-model simulation and real hardware execution.

    Metric: ratio = TVD(ideal, real) / TVD(ideal, noisy)
    - ratio > 1 means real hardware is worse than noise model predicts
    - ratio is independent of circuit length (both terms shrink together)

    Segments are formed by grouping consecutive *moments* (parallel time
    slices) so that each segment contains ``moments_per_segment`` moments.
    Threshold is always adaptive: calibrated from simulator-only runs
    using mean + 2*std - 1.0 of the null ratio distribution.
    """

    # Minimum TVD(ideal, noisy) for a reliable ratio, derived from calibration.
    # Set during _calibrate_noise_threshold as 2 * measured shot noise TVD.
    min_expected_tvd: float = 0.0

    SKIP_OPS = frozenset(["measure", "barrier", "delay", "reset"])

    def __init__(
        self,
        executor,
        test_mode: bool = False,
        max_granularity: int = 16,
        moments_per_segment: Optional[int] = None,
        # --- ablation knobs (all default to current production behavior) ---
        sigma_mult: float = 2.0,
        floor_mult: float = 2.0,
        use_floor: bool = True,
        use_reliability_gate: bool = True,
        oracle_mode: str = "ratio",  # "ratio" | "abs_tvd"
        threshold_mode: str = "calibrated",  # "calibrated" | "fixed" | "none"
        calib_samples: int = 5,
    ) -> None:
        self.executor = executor
        self.test_mode = bool(test_mode)
        self.max_granularity = int(max_granularity)

        raw = moments_per_segment or self._read_config("moments_per_segment")
        if raw is None:
            raise ValueError("Missing execution.delta_debug.moments_per_segment in config")
        self.moments_per_segment = max(1, int(raw))

        # Ablation knobs
        self.sigma_mult = float(sigma_mult)
        self.floor_mult = float(floor_mult)
        self.use_floor = bool(use_floor)
        self.use_reliability_gate = bool(use_reliability_gate)
        self.oracle_mode = oracle_mode  # "ratio" or "abs_tvd"
        self.threshold_mode = threshold_mode  # "calibrated", "fixed", or "none"
        self.calib_samples = int(calib_samples)

        self.original_circuit: Optional[QuantumCircuit] = None
        self.segments: List[Dict[str, Any]] = []
        self.measured_qubits_list: List[int] = []
        self.measure_map: Dict[int, int] = {}
        self.test_count: int = 0
        self.noise_threshold: float = 0.0
        self.ddmin_log: List[Dict[str, Any]] = []

    def _read_config(self, key: str, default=None):
        return self.executor.config.get("execution", {}).get("delta_debug", {}).get(key, default)

    # ---------- segmentation ----------

    def extract_circuit_segments(self, circuit: QuantumCircuit) -> List[Dict[str, Any]]:
        """Partition the circuit into segments of consecutive moments."""
        return segment_circuit(circuit, self.moments_per_segment)

    # ---------- circuit builder ----------

    def build_circuit_without_segments(
        self, original_circuit: QuantumCircuit, segments_to_exclude: Sequence[int],
    ) -> QuantumCircuit:
        try:
            new_circuit = original_circuit.copy_empty_like()
        except Exception:
            new_circuit = QuantumCircuit(original_circuit.num_qubits, original_circuit.num_clbits)

        excluded_indices = {
            inst["index"]
            for seg_idx in segments_to_exclude
            if 0 <= seg_idx < len(self.segments)
            for inst in self.segments[seg_idx]["instructions"]
        }

        for i, inst in enumerate(original_circuit.data):
            if inst.operation.name in self.SKIP_OPS or i in excluded_indices:
                continue
            q_indices = [original_circuit.find_bit(q).index for q in inst.qubits]
            new_circuit.append(inst.operation, [new_circuit.qubits[idx] for idx in q_indices], [])

        for q_idx, c_idx in self.measure_map.items():
            new_circuit.measure(q_idx, c_idx)
        return new_circuit

    # ---------- evaluation ----------

    def evaluate_circuit(
        self, circuit: QuantumCircuit, shots: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Run circuit on ideal, noisy, and real backends. Return ratio metric."""
        self.test_count += 1
        shots = shots or self.executor.config["execution"]["shots"]

        ideal = self.executor.run_circuit(circuit, execution_type="ideal_simulator", shots=shots)
        if not ideal.get("success"):
            raise RuntimeError(f"Ideal execution failed: {ideal.get('error')}")

        noisy = self.executor.run_circuit(circuit, execution_type="noisy_simulator", shots=shots)
        if not noisy.get("success"):
            raise RuntimeError(f"Noisy execution failed: {noisy.get('error')}")

        if self.test_mode:
            real = noisy  # in test mode, "real" = noisy
        else:
            real = self.executor.run_circuit(circuit, execution_type="real_device", shots=shots)
            if not real.get("success"):
                real = self.executor.run_circuit(circuit, execution_type="real_device", shots=shots)
            if not real.get("success"):
                raise RuntimeError(f"Real execution failed: {real.get('error')}")

        expected_tvd, _ = calculate_tvd(ideal["counts"], noisy["counts"])
        actual_tvd, _ = calculate_tvd(ideal["counts"], real["counts"])
        noisy_vs_real, _ = calculate_tvd(noisy["counts"], real["counts"])

        if self.use_reliability_gate:
            reliable = expected_tvd >= self.min_expected_tvd
        else:
            reliable = True  # ablation: skip reliability gate

        if self.oracle_mode == "abs_tvd":
            # Ablation: use absolute TVD(noisy, real) instead of ratio
            ratio = noisy_vs_real
        else:
            ratio = actual_tvd / expected_tvd if expected_tvd > 1e-9 else 1.0

        return {
            "expected_tvd": expected_tvd,
            "actual_tvd": actual_tvd,
            "noisy_vs_real": noisy_vs_real,
            "ratio": ratio,
            "ratio_reliable": reliable,
        }

    # ---------- shot noise calibration ----------

    def _calibrate_noise_threshold(self, circuit: QuantumCircuit, n_samples: int = None) -> float:
        """Measure shot noise in the ratio metric.

        Runs ideal + noisy simulator multiple times (no real device) to see
        how much the ratio fluctuates from pure shot noise.

        Also measures TVD(noisy1, noisy2) -- the raw shot noise floor -- and
        sets min_expected_tvd = floor_mult * mean(shot_noise_tvd). When the
        denominator TVD(ideal, noisy) falls below this, the ratio is noise-dominated.

        Returns mean + sigma_mult*std of ratio variation (the DDMin threshold).
        """
        if n_samples is None:
            n_samples = self.calib_samples
        shots = self.executor.config["execution"]["shots"]
        ratios = []
        shot_noise_tvds = []
        for _ in range(n_samples):
            ideal1 = self.executor.run_circuit(circuit, execution_type="ideal_simulator", shots=shots)
            noisy1 = self.executor.run_circuit(circuit, execution_type="noisy_simulator", shots=shots)
            noisy2 = self.executor.run_circuit(circuit, execution_type="noisy_simulator", shots=shots)

            expected, _ = calculate_tvd(ideal1["counts"], noisy1["counts"])
            actual, _ = calculate_tvd(ideal1["counts"], noisy2["counts"])
            ratio = actual / expected if expected > 1e-9 else 1.0
            ratios.append(ratio)

            sn_tvd, _ = calculate_tvd(noisy1["counts"], noisy2["counts"])
            shot_noise_tvds.append(sn_tvd)

        mean_r = sum(ratios) / len(ratios)
        std_r = (sum((x - mean_r) ** 2 for x in ratios) / len(ratios)) ** 0.5

        mean_sn = sum(shot_noise_tvds) / len(shot_noise_tvds)
        if self.use_floor:
            self.min_expected_tvd = self.floor_mult * mean_sn
        else:
            self.min_expected_tvd = 0.0  # ablation: no floor

        return mean_r + self.sigma_mult * std_r - 1.0

    # ---------- DDMin ----------

    def _test_exclusion(
        self, excluded: List[int], kept: List[int], action: str,
        baseline_ratio: float, shots: int,
    ) -> Dict[str, Any]:
        circ = self.build_circuit_without_segments(self.original_circuit, excluded)
        result = self.evaluate_circuit(circ, shots=shots)
        reduction = baseline_ratio - result["ratio"]
        return {
            "action": action,
            "excluded": excluded,
            "kept": kept,
            "ratio": round(result["ratio"], 4),
            "ratio_reliable": result["ratio_reliable"],
            "baseline_ratio": round(baseline_ratio, 4),
            "reduction": round(reduction, 4),
            "noise_threshold": round(self.noise_threshold, 4),
            "progressed": False,
            "result": "",
        }

    def ddmin(
        self, baseline_ratio: float, initial_candidates: Optional[List[int]] = None,
    ) -> List[int]:
        """DDMin algorithm with three narrowing cases per the paper.

        For each partition (subset, complement):
          1. Drop(subset): remove subset, keep complement -> if ratio drops
             by more than tau, subset was problematic -> narrow into subset.
          2. Drop(complement): remove complement, keep subset -> if ratio drops
             by more than tau, complement was problematic -> narrow into complement.
          3. Sufficient(subset): if retaining only subset preserves
             R > 1 + tau, subset is sufficient -> narrow into subset.
        """
        shots = self.executor.config["execution"]["shots"]
        candidates = (
            initial_candidates if initial_candidates is not None
            else list(range(len(self.segments)))
        )
        n = 2

        while len(candidates) >= 2:
            subsets = self._split(candidates, n)
            progressed = False

            for subset in subsets:
                complement = [i for i in candidates if i not in subset]
                if not complement:
                    continue

                # Case 1: Drop(subset) -- remove subset, keep complement
                entry_sub = self._test_exclusion(
                    subset, complement, "test_subset", baseline_ratio, shots,
                )
                if entry_sub["ratio_reliable"] and entry_sub["reduction"] > self.noise_threshold:
                    entry_sub["progressed"] = True
                    entry_sub["result"] = (
                        f"remove segs {self._fmt_range(subset)}: "
                        f"drop={entry_sub['reduction']:.3f} > tau={self.noise_threshold:.3f} "
                        f"-> narrow to {self._fmt_range(subset)}"
                    )
                    self.ddmin_log.append(entry_sub)
                    candidates = subset
                    progressed = True
                if progressed:
                    break

                # Case 2: Drop(complement) -- remove complement, keep subset
                entry_comp = self._test_exclusion(
                    complement, subset, "test_complement", baseline_ratio, shots,
                )
                if not entry_comp["ratio_reliable"]:
                    pass
                elif entry_comp["reduction"] > self.noise_threshold:
                    entry_comp["progressed"] = True
                    entry_comp["result"] = (
                        f"remove segs {self._fmt_range(complement)}: "
                        f"drop={entry_comp['reduction']:.3f} > tau={self.noise_threshold:.3f} "
                        f"-> narrow to {self._fmt_range(complement)}"
                    )
                    self.ddmin_log.append(entry_comp)
                    candidates = complement
                    progressed = True
                elif (
                    len(subset) < len(candidates)
                    and entry_comp["ratio"] > 1.0 + self.noise_threshold
                ):
                    entry_comp["progressed"] = True
                    entry_comp["action"] = "sufficient"
                    entry_comp["result"] = (
                        f"keep segs {self._fmt_range(subset)}: "
                        f"ratio={entry_comp['ratio']:.3f} > 1+tau={1.0+self.noise_threshold:.3f} "
                        f"-> sufficient, narrow to {self._fmt_range(subset)}"
                    )
                    self.ddmin_log.append(entry_comp)
                    candidates = subset
                    progressed = True
                if progressed:
                    break

            if progressed:
                n = 2
            elif n < min(self.max_granularity, len(candidates)):
                n = min(n * 2, len(candidates))
            else:
                break

        return candidates

    @staticmethod
    def _fmt_range(ids: List[int]) -> str:
        """Format a list of segment IDs as a compact range string."""
        if not ids:
            return "[]"
        ids = sorted(ids)
        if ids == list(range(ids[0], ids[-1] + 1)):
            return f"{ids[0]}-{ids[-1]}" if len(ids) > 1 else str(ids[0])
        return str(ids)

    @staticmethod
    def _split(items: List[int], n: int) -> List[List[int]]:
        if n >= len(items):
            return [[x] for x in items]
        size, rem = divmod(len(items), n)
        out, start = [], 0
        for i in range(n):
            end = start + size + (1 if i < rem else 0)
            out.append(items[start:end])
            start = end
        return out

    # ---------- pattern extraction ----------

    @staticmethod
    def _extract_pattern(circuit: QuantumCircuit, segments: List[Dict[str, Any]],
                         minimal_ids: List[int]) -> List[tuple]:
        """Extract the gate subsequence from the minimal segments as a token list.

        Each token is (gate_name, (qubit_indices...), (params...)), matching
        the normalize_token format used elsewhere in the codebase.
        Tokens are sorted by their original circuit index to preserve ordering.
        """
        insts_with_idx = []
        for seg_idx in sorted(minimal_ids):
            if seg_idx >= len(segments):
                continue
            for inst in segments[seg_idx]["instructions"]:
                idx = inst.get("index", 0)
                params = []
                for p in inst.get("params", []):
                    try:
                        params.append(round(float(p), 6))
                    except Exception:
                        params.append(str(p))
                insts_with_idx.append((idx, (
                    inst["operation"],
                    tuple(inst["qubits"]),
                    tuple(params),
                )))
        insts_with_idx.sort(key=lambda x: x[0])
        return [tok for _, tok in insts_with_idx]

    def _build_result(self, candidates: List[int]) -> Dict[str, Any]:
        pattern = self._extract_pattern(
            self.original_circuit, self.segments, candidates,
        ) if candidates else []
        return {
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "circuit_info": {
                    "total_qubits": self.original_circuit.num_qubits,
                    "measured_qubits": self.measured_qubits_list,
                },
                "measurement_mapping": self.measure_map,
                "evaluation": {
                    "shots": self.executor.config["execution"]["shots"],
                    "noise_threshold": self.noise_threshold,
                    "min_expected_tvd": self.min_expected_tvd,
                    "max_granularity": self.max_granularity,
                    "moments_per_segment": self.moments_per_segment,
                    "test_mode": self.test_mode,
                },
            },
            "problematic_segments": candidates,
            "pattern": [list(tok) for tok in pattern],
            "segments_info": self.segments,
            "ddmin_log": self.ddmin_log,
        }

    # ---------- public API ----------

    def debug_circuit(
        self,
        circuit: QuantumCircuit,
    ) -> Dict[str, Any]:
        self.original_circuit = circuit

        # Extract measurements
        self.measure_map = {}
        for inst in circuit.data:
            if inst.operation.name == "measure":
                self.measure_map[circuit.find_bit(inst.qubits[0]).index] = circuit.find_bit(inst.clbits[0]).index
        if not self.measure_map:
            raise ValueError("Circuit has no measurement operations.")
        self.measured_qubits_list = sorted(self.measure_map)

        self.test_count = 0
        self.ddmin_log.clear()
        self.segments = self.extract_circuit_segments(circuit)

        # Baseline
        full = self.build_circuit_without_segments(circuit, [])
        baseline = self.evaluate_circuit(full)

        # Calibrate noise threshold
        if self.threshold_mode == "calibrated":
            print("Calibrating noise threshold...", flush=True)
            self.noise_threshold = self._calibrate_noise_threshold(full)
        elif self.threshold_mode == "fixed":
            self.noise_threshold = 0.05  # fixed ablation threshold
        else:
            # threshold_mode == "none": no threshold (tau = 0)
            self.noise_threshold = 0.0
            self.min_expected_tvd = 0.0
        print(
            f"  Baseline ratio = {baseline['ratio']:.3f} "
            f"(expected_tvd={baseline['expected_tvd']:.4f}, actual_tvd={baseline['actual_tvd']:.4f}), "
            f"noise threshold = {self.noise_threshold:.4f}, "
            f"min_expected_tvd = {self.min_expected_tvd:.4f}",
            flush=True,
        )

        # Early exit: ratio ~ 1.0 means noise model is accurate
        if baseline["ratio"] <= 1.0 + self.noise_threshold:
            print(
                f"  Baseline ratio ({baseline['ratio']:.3f}) within noise floor "
                f"({1.0 + self.noise_threshold:.3f}). "
                f"Noisy simulator is accurate; skipping DDMin.",
                flush=True,
            )
            self.ddmin_log.append({
                "action": "baseline",
                "kept": len(self.segments),
                "ratio": round(baseline["ratio"], 4),
                "noise_threshold": round(self.noise_threshold, 4),
                "result": (
                    f"ratio={baseline['ratio']:.3f} <= 1+tau={1.0+self.noise_threshold:.3f}, "
                    f"noise model is accurate; skipping DDMin"
                ),
            })
            return self._build_result([])

        self.ddmin_log.append({
            "action": "baseline",
            "kept": len(self.segments),
            "ratio": round(baseline["ratio"], 4),
            "noise_threshold": round(self.noise_threshold, 4),
            "result": (
                f"ratio={baseline['ratio']:.3f} > 1+tau={1.0+self.noise_threshold:.3f}, "
                f"unmodeled error detected; starting DDMin on {len(self.segments)} segments"
            ),
        })

        minimal = self.ddmin(baseline["ratio"])
        return self._build_result(minimal)

    def save_debug_report(self, result: Dict[str, Any], filename: Optional[str] = None) -> str:
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2, default=str)
        return filename


def run_delta_debug_on_isa(
    executor,
    isa_circuit: QuantumCircuit,
    test_mode: bool = False,
    max_granularity: int = 16,
    moments_per_segment: Optional[int] = None,
    # --- ablation knobs (all default to current production behavior) ---
    sigma_mult: float = 2.0,
    floor_mult: float = 2.0,
    use_floor: bool = True,
    use_reliability_gate: bool = True,
    oracle_mode: str = "ratio",
    threshold_mode: str = "calibrated",
    calib_samples: int = 5,
) -> Dict[str, Any]:
    dbg = QuantumDeltaDebugger(
        executor=executor,
        test_mode=test_mode,
        max_granularity=max_granularity,
        moments_per_segment=moments_per_segment,
        sigma_mult=sigma_mult,
        floor_mult=floor_mult,
        use_floor=use_floor,
        use_reliability_gate=use_reliability_gate,
        oracle_mode=oracle_mode,
        threshold_mode=threshold_mode,
        calib_samples=calib_samples,
    )
    return dbg.debug_circuit(isa_circuit)


def aggregate_reports(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate multiple single-run DDMin results into segment frequency scores.

    Each DDMin run finds one problematic region. Running K times and counting
    how often each segment is flagged produces a reliability score per segment.

    Returns a dict with:
      - segment_scores: list of {segment_id, flagged_count, frequency, description}
        sorted by frequency descending
      - total_runs: number of runs aggregated
      - segments_info: segment definitions (from the first result)
      - runs: per-run summaries (problematic segments, baseline ratio, etc.)
    """
    if not results:
        return {"segment_scores": [], "total_runs": 0, "segments_info": [], "runs": []}

    segments_info = results[0]["segments_info"]
    total_segments = len(segments_info)
    total_runs = len(results)

    counts: Dict[int, int] = {}
    for seg_idx in range(total_segments):
        counts[seg_idx] = 0

    runs = []
    for i, result in enumerate(results):
        problematic = result.get("problematic_segments", [])
        for seg_idx in problematic:
            if seg_idx in counts:
                counts[seg_idx] += 1

        baseline_entry = None
        for entry in result.get("ddmin_log", []):
            if entry.get("action") == "baseline":
                baseline_entry = entry
                break

        runs.append({
            "run": i + 1,
            "problematic_segments": problematic,
            "pattern": result.get("pattern", []),
            "baseline_ratio": baseline_entry.get("ratio") if baseline_entry else None,
            "noise_threshold": baseline_entry.get("noise_threshold") if baseline_entry else None,
            "steps": len(result.get("ddmin_log", [])),
        })

    segment_scores = []
    for seg_idx in range(total_segments):
        if counts[seg_idx] > 0:
            seg = segments_info[seg_idx] if seg_idx < len(segments_info) else {}
            segment_scores.append({
                "segment_id": seg_idx,
                "flagged_count": counts[seg_idx],
                "frequency": counts[seg_idx] / total_runs,
                "description": seg.get("description", ""),
            })

    segment_scores.sort(key=lambda x: (-x["frequency"], x["segment_id"]))

    return {
        "segment_scores": segment_scores,
        "total_runs": total_runs,
        "segments_info": segments_info,
        "runs": runs,
    }
