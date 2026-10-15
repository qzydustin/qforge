"""Connection to IBM Quantum across the configured accounts, plus the
account-level operations behind scripts/ibm_accounts.py."""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from qiskit_ibm_runtime import QiskitRuntimeService

PENDING_STATES = {"INITIALIZING", "QUEUED", "RUNNING", "VALIDATING"}
FINAL_STATES = {"DONE", "CANCELLED", "ERROR"}

# Suppress repetitive QiskitRuntimeService token-loading warning.
logging.getLogger("qiskit_ibm_runtime.qiskit_runtime_service").setLevel(logging.ERROR)
logging.getLogger("qiskit_runtime_service").setLevel(logging.ERROR)


class QuantumServiceManager:
    """Handles connection to IBM Quantum and backend selection."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.service: Optional[QiskitRuntimeService] = None
        self.backend = None
        self.last_connect_error: Optional[Exception] = None
        self.selected_account: Optional[Dict[str, Any]] = None
        self.account_rankings: List[Dict[str, Any]] = []

    @staticmethod
    def _masked_account_name(account: Dict[str, Any], index: int) -> str:
        name = str(account.get("name") or f"account-{index + 1}")
        return name

    def _build_service_kwargs(self, account: Dict[str, Any]) -> Dict[str, Any]:
        cfg = self.config["ibm_quantum"]
        kwargs: Dict[str, Any] = {
            "channel": account.get("channel") or cfg.get("channel"),
            "token": account["token"],
            "instance": account.get("instance") or cfg.get("instance"),
        }
        url = account.get("url") or cfg.get("url")
        if url:
            kwargs["url"] = url
        return kwargs

    def _configured_accounts(self) -> List[Dict[str, Any]]:
        cfg = self.config["ibm_quantum"]
        accounts = [dict(account) for account in (cfg.get("accounts") or [])]

        if accounts:
            return accounts

        token = cfg.get("token")
        if not token:
            return []

        return [
            {
                "name": cfg.get("name") or "default",
                "token": token,
                "channel": cfg.get("channel"),
                "instance": cfg.get("instance"),
                "url": cfg.get("url"),
                "backend": cfg.get("backend"),
            }
        ]

    def _connect_single(self, account: Dict[str, Any], index: int) -> Dict[str, Any]:
        kwargs = self._build_service_kwargs(account)
        service = QiskitRuntimeService(**kwargs)
        usage_raw = _safe_call(service, "usage", default=None)
        usage = _to_jsonable(usage_raw)
        remaining_seconds = _extract_remaining_seconds(usage)
        return {
            "index": index,
            "name": self._masked_account_name(account, index),
            "service": service,
            "remaining_seconds": remaining_seconds,
            "usage": usage,
            "channel": kwargs.get("channel"),
            "instance": kwargs.get("instance"),
            "backend": account.get("backend"),
        }

    def connect(self) -> bool:
        """Connect to IBM Quantum service using config credentials."""
        cfg = self.config["ibm_quantum"]
        accounts = self._configured_accounts()
        min_remaining_seconds = _as_float(cfg.get("min_remaining_seconds"))
        if min_remaining_seconds is None:
            min_remaining_seconds = 15.0

        if not accounts:
            self.last_connect_error = ValueError(
                "No IBM accounts configured (set ibm_quantum.accounts or ibm_quantum.token)"
            )
            print(f"Failed to connect: {self.last_connect_error}")
            return False

        connected: List[Dict[str, Any]] = []
        failures: List[Dict[str, Any]] = []

        for idx, account in enumerate(accounts):
            if not account.get("token"):
                failures.append(
                    {
                        "index": idx,
                        "name": self._masked_account_name(account, idx),
                        "error": "missing token",
                    }
                )
                continue

            try:
                connected.append(self._connect_single(account, idx))
            except Exception as e:
                failures.append(
                    {
                        "index": idx,
                        "name": self._masked_account_name(account, idx),
                        "error": str(e),
                    }
                )

        if not connected:
            msg = "No IBM accounts could be connected"
            if failures:
                msg += ": " + "; ".join(f"{f['name']} ({f['error']})" for f in failures)
            self.last_connect_error = RuntimeError(msg)
            print(f"Failed to connect: {self.last_connect_error}")
            return False

        def score(item: Dict[str, Any]) -> float:
            val = item.get("remaining_seconds")
            return float(val) if isinstance(val, (int, float)) else float("-inf")

        self.account_rankings = sorted(
            [
                {
                    "index": item["index"],
                    "name": item["name"],
                    "remaining_seconds": item.get("remaining_seconds"),
                }
                for item in connected
            ],
            key=lambda x: score(x),
            reverse=True,
        )

        eligible = [
            item
            for item in connected
            if isinstance(item.get("remaining_seconds"), (int, float))
            and float(item["remaining_seconds"]) > float(min_remaining_seconds)
        ]

        # If no account passes threshold, fall back to max remaining.
        candidates = eligible if eligible else connected
        chosen = sorted(candidates, key=score, reverse=True)[0]

        self.service = chosen["service"]
        self.selected_account = {
            "index": chosen["index"],
            "name": chosen["name"],
            "remaining_seconds": chosen.get("remaining_seconds"),
            "channel": chosen.get("channel"),
            "instance": chosen.get("instance"),
            "backend": chosen.get("backend"),
            "threshold_seconds": min_remaining_seconds,
            "threshold_passed": chosen in eligible,
        }
        self.last_connect_error = None

        selected_rem = self.selected_account.get("remaining_seconds")
        rem_text = f"{selected_rem:.2f}s" if isinstance(selected_rem, (int, float)) else "unknown"
        print(
            f"Selected IBM account: {self.selected_account['name']} "
            f"(remaining={rem_text})"
        )
        return True

    def select_backend(self, name: Optional[str] = None):
        """Select backend by name (defaults to config or selected account value)."""
        if not self.service:
            return None

        cfg_backend = self.config["ibm_quantum"].get("backend")
        selected_backend = (self.selected_account or {}).get("backend")
        backend_name = name or selected_backend or cfg_backend
        try:
            self.backend = self.service.backend(backend_name)
            return self.backend
        except Exception as e:
            print(f"Failed to select backend {backend_name}: {e}")
            return None


def _safe_call(obj: Any, attr: str, *args, default=None, **kwargs):
    if obj is None or not hasattr(obj, attr):
        return default
    target = getattr(obj, attr)
    try:
        return target(*args, **kwargs) if callable(target) else target
    except Exception:
        return default


def _status_name(status: Any) -> str:
    if status is None:
        return "UNKNOWN"
    if hasattr(status, "name"):
        return str(status.name)
    text = str(status)
    return text.split(".")[-1].upper()


def _to_jsonable(value: Any):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_to_jsonable(v) for v in value]
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        out = {}
        for k, v in vars(value).items():
            if not str(k).startswith("_"):
                out[str(k)] = _to_jsonable(v)
        if out:
            return out
    return str(value)


def _as_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value)
    except Exception:
        return None


def _extract_remaining_seconds(usage: Any) -> Optional[float]:
    if not isinstance(usage, dict):
        return None

    remaining_seconds = _as_float(usage.get("usage_remaining_seconds"))
    if remaining_seconds is not None:
        return max(remaining_seconds, 0.0)

    consumed_seconds = _as_float(usage.get("usage_consumed_seconds"))
    limit_seconds = _as_float(usage.get("usage_limit_seconds"))
    if consumed_seconds is not None and limit_seconds is not None:
        return max(limit_seconds - consumed_seconds, 0.0)

    return None


def list_account_remaining(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """One row per configured account, most remaining QPU time first."""
    manager = QuantumServiceManager(config)
    cfg = config["ibm_quantum"]
    rows: List[Dict[str, Any]] = []
    for idx, account in enumerate(manager._configured_accounts()):
        row = {
            "index": idx,
            "name": manager._masked_account_name(account, idx),
            "remaining_seconds": None,
            "remaining_minutes": None,
            "channel": account.get("channel") or cfg.get("channel"),
            "instance": account.get("instance") or cfg.get("instance"),
            "backend": account.get("backend") or cfg.get("backend"),
            "error": None,
        }
        if not account.get("token"):
            row["error"] = "missing token"
        else:
            try:
                remaining = manager._connect_single(account, idx)["remaining_seconds"]
            except Exception as e:
                row["error"] = str(e)
            else:
                row["remaining_seconds"] = remaining
                if isinstance(remaining, (int, float)):
                    row["remaining_minutes"] = remaining / 60.0
        rows.append(row)

    def score(row: Dict[str, Any]) -> float:
        val = row.get("remaining_seconds")
        return float(val) if isinstance(val, (int, float)) else float("-inf")

    return sorted(rows, key=score, reverse=True)


def cancel_jobs_for_account(
    config: Dict[str, Any],
    account: Dict[str, Any],
    limit: int = 100,
    dry_run: bool = True,
) -> List[Dict[str, Any]]:
    """Cancel the pending jobs among the account's ``limit`` most recent jobs.

    A dry run only lists them: one status lookup per job, nothing else.
    """
    if not account.get("token"):
        raise ValueError(f"Account '{account.get('name')}' has no token")
    service = QiskitRuntimeService(**QuantumServiceManager(config)._build_service_kwargs(account))

    results: List[Dict[str, Any]] = []
    for job in service.jobs(limit=limit):
        status = _status_name(_safe_call(job, "status"))
        if status not in PENDING_STATES:
            continue
        if not dry_run:
            # Re-read: the job may have finished since it was listed, and cancelling a final job raises.
            status = _status_name(_safe_call(job, "status"))
        result = {
            "job_id": job.job_id(),
            "status_before": status,
            "cancel_called": False,
            "status_after": status,
        }
        if not dry_run and status not in FINAL_STATES:
            job.cancel()
            time.sleep(1.0)
            result["cancel_called"] = True
            result["status_after"] = _status_name(_safe_call(job, "status"))
        results.append(result)
    return results
