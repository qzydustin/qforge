from __future__ import annotations

from dataclasses import dataclass
import json
import logging
from pathlib import Path
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

    def __init__(self, config_file: str = "quantum_config.json"):
        self.config = self._load_config(config_file)
        self.service: Optional[QiskitRuntimeService] = None
        self.backend = None
        self.last_connect_error: Optional[Exception] = None
        self.selected_account: Optional[Dict[str, Any]] = None
        self.account_rankings: List[Dict[str, Any]] = []

    @staticmethod
    def _load_config(config_file: str) -> Dict[str, Any]:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)

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


@dataclass
class RuntimeOpsClient:
    repo_root: Path
    config_path: Path
    config: Dict[str, Any]
    manager: QuantumServiceManager
    service: Any
    backend: Any


def _safe_call(obj: Any, attr: str, *args, default=None, **kwargs):
    if obj is None or not hasattr(obj, attr):
        return default
    target = getattr(obj, attr)
    try:
        return target(*args, **kwargs) if callable(target) else target
    except Exception:
        return default


def _backend_name(backend: Any) -> Optional[str]:
    if backend is None:
        return None
    name = getattr(backend, "name", None)
    return name() if callable(name) else name


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


def _resolve_config_path(config_path: str | Path | None = None) -> Path:
    if config_path is not None:
        path = Path(config_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"Config not found: {path}")
        return path

    cwd = Path.cwd().resolve()
    for base in (cwd, *cwd.parents):
        candidate = base / "quantum_config.json"
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "Cannot find quantum_config.json; please run from repo or pass config_path"
    )


def _resolve_named_account(
    manager: QuantumServiceManager,
    account_name: str,
) -> tuple[int, Dict[str, Any], str]:
    target = (account_name or "").strip()
    if not target:
        raise ValueError("account_name is required")

    accounts = manager._configured_accounts()
    if not accounts:
        raise ValueError("No IBM accounts configured")

    for idx, account in enumerate(accounts):
        name = manager._masked_account_name(account, idx)
        if name == target:
            return idx, account, name

    target_lower = target.lower()
    for idx, account in enumerate(accounts):
        name = manager._masked_account_name(account, idx)
        if name.lower() == target_lower:
            return idx, account, name

    available = ", ".join(
        manager._masked_account_name(account, idx)
        for idx, account in enumerate(accounts)
    )
    raise ValueError(f"Account not found: {account_name}. Available: {available}")


def list_account_remaining(
    config_path: str | Path | None = None,
) -> List[Dict[str, Any]]:
    resolved = _resolve_config_path(config_path)
    manager = QuantumServiceManager(config_file=str(resolved))
    accounts = manager._configured_accounts()

    rows: List[Dict[str, Any]] = []
    for idx, account in enumerate(accounts):
        name = manager._masked_account_name(account, idx)
        if not account.get("token"):
            rows.append(
                {
                    "index": idx,
                    "name": name,
                    "remaining_seconds": None,
                    "remaining_minutes": None,
                    "channel": account.get("channel") or manager.config["ibm_quantum"].get("channel"),
                    "instance": account.get("instance") or manager.config["ibm_quantum"].get("instance"),
                    "backend": account.get("backend") or manager.config["ibm_quantum"].get("backend"),
                    "error": "missing token",
                }
            )
            continue

        try:
            item = manager._connect_single(account, idx)
            remaining_seconds = item.get("remaining_seconds")
            rows.append(
                {
                    "index": idx,
                    "name": item["name"],
                    "remaining_seconds": remaining_seconds,
                    "remaining_minutes": (
                        remaining_seconds / 60.0
                        if isinstance(remaining_seconds, (int, float))
                        else None
                    ),
                    "channel": item.get("channel"),
                    "instance": item.get("instance"),
                    "backend": item.get("backend") or manager.config["ibm_quantum"].get("backend"),
                    "error": None,
                }
            )
        except Exception as e:
            rows.append(
                {
                    "index": idx,
                    "name": name,
                    "remaining_seconds": None,
                    "remaining_minutes": None,
                    "channel": account.get("channel") or manager.config["ibm_quantum"].get("channel"),
                    "instance": account.get("instance") or manager.config["ibm_quantum"].get("instance"),
                    "backend": account.get("backend") or manager.config["ibm_quantum"].get("backend"),
                    "error": str(e),
                }
            )

    def score(row: Dict[str, Any]) -> float:
        val = row.get("remaining_seconds")
        return float(val) if isinstance(val, (int, float)) else float("-inf")

    return sorted(rows, key=score, reverse=True)


def create_runtime_client_for_account(
    account_name: str,
    config_path: str | Path | None = None,
) -> RuntimeOpsClient:
    resolved = _resolve_config_path(config_path)
    repo_root = resolved.parent
    config = json.loads(resolved.read_text(encoding="utf-8"))

    manager = QuantumServiceManager(config_file=str(resolved))
    idx, account, resolved_name = _resolve_named_account(manager, account_name)
    if not account.get("token"):
        raise ValueError(f"Account '{resolved_name}' has no token")

    connected = manager._connect_single(account, idx)
    manager.service = connected["service"]
    manager.selected_account = {
        "index": connected["index"],
        "name": connected["name"],
        "remaining_seconds": connected.get("remaining_seconds"),
        "channel": connected.get("channel"),
        "instance": connected.get("instance"),
        "backend": connected.get("backend"),
    }

    backend_name = connected.get("backend") or config.get("ibm_quantum", {}).get("backend")
    backend = None
    if backend_name:
        try:
            backend = manager.service.backend(backend_name)
        except Exception:
            backend = None
    manager.backend = backend

    return RuntimeOpsClient(
        repo_root=repo_root,
        config_path=resolved,
        config=config,
        manager=manager,
        service=manager.service,
        backend=backend,
    )


def list_jobs_for_account(
    account_name: str,
    config_path: str | Path | None = None,
    limit: int = 50,
    pending: bool | None = None,
) -> List[Dict[str, Any]]:
    client = create_runtime_client_for_account(
        account_name=account_name,
        config_path=config_path,
    )
    return list_jobs(client=client, limit=limit, pending=pending)


def cancel_jobs_for_account(
    account_name: str,
    config_path: str | Path | None = None,
    limit: int = 100,
    dry_run: bool = True,
    include_running: bool = True,
    wait_seconds: float = 1.0,
) -> List[Dict[str, Any]]:
    client = create_runtime_client_for_account(
        account_name=account_name,
        config_path=config_path,
    )
    records = list_jobs(client=client, limit=limit, pending=None)

    target_states = set(PENDING_STATES)
    if not include_running:
        target_states.discard("RUNNING")

    targets: List[Dict[str, Any]] = []
    for record in records:
        status = str(record.get("status") or "UNKNOWN")
        if status not in target_states:
            continue
        if not record.get("job_id"):
            continue
        targets.append(record)

    results: List[Dict[str, Any]] = []

    if dry_run:
        # Preview only: avoid per-job round trips that can make notebook feel stuck.
        for record in targets:
            status_before = str(record.get("status") or "UNKNOWN")
            results.append(
                {
                    "job_id": str(record["job_id"]),
                    "status_before": status_before,
                    "cancel_called": False,
                    "status_after": status_before,
                }
            )
        return results

    for record in targets:
        results.append(
            cancel_job(
                client=client,
                job_id=str(record["job_id"]),
                dry_run=False,
                wait_seconds=wait_seconds,
            )
        )
    return results


def _queue_fields(job: Any) -> Dict[str, Any]:
    qi = _safe_call(job, "queue_info", default=None)

    if qi is None:
        return {
            "queue_position": None,
            "estimated_start_time": None,
            "estimated_complete_time": None,
        }

    if isinstance(qi, dict):
        src = qi
    else:
        src = _to_jsonable(qi)
        if not isinstance(src, dict):
            src = {}

    return {
        "queue_position": src.get("position") or src.get("queue_position"),
        "estimated_start_time": src.get("estimated_start_time"),
        "estimated_complete_time": src.get("estimated_complete_time"),
    }


def _job_id(job: Any) -> Optional[str]:
    jid = _safe_call(job, "job_id", default=None)
    if jid is not None:
        return str(jid)
    text = str(getattr(job, "job_id", ""))
    return text or None


def _job_record(job: Any) -> Dict[str, Any]:
    backend_obj = _safe_call(job, "backend", default=None)
    created = _safe_call(job, "creation_date", default=None)

    record = {
        "job_id": _job_id(job),
        "status": _status_name(_safe_call(job, "status", default=None)),
        "backend": _backend_name(backend_obj),
        "created": _to_jsonable(created),
        "session_id": _safe_call(job, "session_id", default=None),
    }
    record.update(_queue_fields(job))
    return record


def _fetch_jobs_raw(
    client: RuntimeOpsClient,
    limit: int = 30,
    pending: bool | None = None,
) -> List[Any]:
    kwargs = {"limit": limit}
    if pending is not None:
        kwargs["pending"] = pending

    try:
        jobs = list(client.service.jobs(**kwargs))
    except TypeError:
        kwargs.pop("pending", None)
        jobs = list(client.service.jobs(**kwargs))

    if pending is not None:
        filtered = []
        for job in jobs:
            status = _status_name(_safe_call(job, "status", default=None))
            is_pending = status in PENDING_STATES
            if (pending and is_pending) or ((pending is False) and (not is_pending)):
                filtered.append(job)
        jobs = filtered

    return jobs


def list_jobs(
    client: RuntimeOpsClient,
    limit: int = 30,
    pending: bool | None = None,
) -> List[Dict[str, Any]]:
    jobs = _fetch_jobs_raw(client=client, limit=limit, pending=pending)
    return [_job_record(job) for job in jobs]


def cancel_job(
    client: RuntimeOpsClient,
    job_id: str,
    dry_run: bool = True,
    wait_seconds: float = 1.0,
) -> Dict[str, Any]:
    job = client.service.job(job_id)
    status_before = _status_name(_safe_call(job, "status", default=None))

    result = {
        "job_id": job_id,
        "status_before": status_before,
        "cancel_called": False,
        "status_after": status_before,
    }

    if status_before in FINAL_STATES:
        return result

    if dry_run:
        return result

    job.cancel()
    if wait_seconds > 0:
        time.sleep(wait_seconds)

    status_after = _status_name(_safe_call(job, "status", default=None))
    result["cancel_called"] = True
    result["status_after"] = status_after
    return result


