"""
QPU-time budget guard for QRisk hardware experiments.

Every real-device job is checked against a hard cap *before* submission and
its measured usage is appended to a JSONL ledger *after* completion.  The
ledger persists across processes, so the cap holds even if a script crashes
and is restarted, or several scripts share one budget.

The cap is conservative: before a job is submitted we require
    spent + estimated_cost(next job) <= cap
where the estimate is the largest per-circuit cost observed so far (or a
pessimistic default before the first job) times the number of circuits.
"""

from __future__ import annotations

import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class BudgetExceeded(RuntimeError):
    """Raised when submitting the next job could exceed the QPU-time cap."""


class QPUBudget:
    def __init__(
        self,
        ledger_path: str | Path,
        cap_seconds: float,
        default_seconds_per_circuit: float = 10.0,
    ) -> None:
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self.cap_seconds = float(cap_seconds)
        self.default_seconds_per_circuit = float(default_seconds_per_circuit)
        # Seconds reserved by jobs that passed check() but are not yet
        # recorded (jobs in flight from parallel threads).
        self._reserved = 0.0
        self._lock = threading.Lock()

    # ---------- ledger ----------

    def entries(self) -> list[Dict[str, Any]]:
        if not self.ledger_path.exists():
            return []
        rows = []
        with self.ledger_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows

    def spent_seconds(self) -> float:
        return sum(float(e.get("seconds") or 0.0) for e in self.entries())

    def remaining_seconds(self) -> float:
        return self.cap_seconds - self.spent_seconds() - self._reserved

    def seconds_per_circuit_estimate(self) -> float:
        per_circuit = [
            float(e["seconds"]) / max(1, int(e.get("n_circuits", 1)))
            for e in self.entries()
            if e.get("seconds") is not None and e.get("measured", True)
        ]
        if not per_circuit:
            return self.default_seconds_per_circuit
        return max(per_circuit)

    # ---------- guard ----------

    def check(self, n_circuits: int = 1, label: str = "", reserve: bool = False) -> float:
        """Raise BudgetExceeded if the next job could push spending over the cap.

        Returns the estimated cost of the job in seconds.  With
        ``reserve=True`` the estimate is held until ``record(reservation=...)``
        so concurrent threads cannot jointly overshoot the cap.
        """
        with self._lock:
            estimate = self.seconds_per_circuit_estimate() * max(1, n_circuits)
            spent = self.spent_seconds() + self._reserved
            if spent + estimate > self.cap_seconds:
                raise BudgetExceeded(
                    f"QPU budget stop before '{label}': spent/in-flight {spent:.1f}s + "
                    f"estimated {estimate:.1f}s > cap {self.cap_seconds:.1f}s"
                )
            if reserve:
                self._reserved += estimate
            return estimate

    def record(
        self,
        seconds: Optional[float],
        n_circuits: int,
        backend: Optional[str],
        job_id: Optional[str],
        label: str = "",
        measured: bool = True,
        shots: Optional[int] = None,
        reservation: float = 0.0,
    ) -> None:
        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "label": label,
            "backend": backend,
            "job_id": job_id,
            "n_circuits": n_circuits,
            "shots": shots,
            "seconds": seconds,
            "measured": measured,
        }
        with self._lock:
            with self.ledger_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            self._reserved = max(0.0, self._reserved - reservation)

    def summary(self) -> str:
        spent = self.spent_seconds()
        return (
            f"QPU spent {spent:.1f}s ({spent / 60:.1f} min) of cap "
            f"{self.cap_seconds:.0f}s ({self.cap_seconds / 60:.0f} min); "
            f"{len(self.entries())} jobs; "
            f"est. {self.seconds_per_circuit_estimate():.1f}s per circuit"
        )


def job_usage_seconds(job) -> tuple[Optional[float], bool]:
    """Best-effort QPU usage of a finished runtime job.

    Returns (seconds, measured).  ``measured`` is False when usage could not
    be read and the caller should fall back to an estimate.
    """
    try:
        val = job.usage()
        if val is not None:
            return float(val), True
    except Exception:
        pass
    try:
        usage = (job.metrics() or {}).get("usage", {})
        for key in ("quantum_seconds", "seconds"):
            if usage.get(key) is not None:
                return float(usage[key]), True
    except Exception:
        pass
    return None, False
