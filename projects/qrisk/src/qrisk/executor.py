from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime import SamplerV2 as RuntimeSampler

from .budget import BudgetExceeded, QPUBudget, job_usage_seconds
from .config import load_config
from .ibm_runtime import QuantumServiceManager
from .paths import CONFIG_FILE

# Offline stand-ins for the IBM backends (used only with hardware="emulate").
_FAKE_BACKENDS = {
    "ibm_fez": "FakeFez",
    "ibm_marrakesh": "FakeMarrakesh",
    "ibm_torino": "FakeTorino",
    # No FakeKingston ships with qiskit-ibm-runtime; Fez is the same Heron r2 topology.
    "ibm_kingston": "FakeFez",
}

# Seconds charged to the dry-run ledger per emulated circuit, so the budget
# guard can be exercised offline.
EMULATED_SECONDS_PER_CIRCUIT = 2.0


def _fake_backend(name: str):
    from qiskit_ibm_runtime import fake_provider
    cls_name = _FAKE_BACKENDS.get(name)
    if cls_name is None:
        raise ValueError(f"No offline fake backend for {name}; choose one of {sorted(_FAKE_BACKENDS)}")
    return getattr(fake_provider, cls_name)()


def _pub_counts(pub_result) -> Dict[str, int]:
    # join_data() merges all classical registers (e.g. MQT's "meas" plus any others).
    try:
        return pub_result.join_data().get_counts()
    except Exception:
        pass
    for bit_array in pub_result.data.values():
        if hasattr(bit_array, "get_counts"):
            return bit_array.get_counts()
    return {}


def _sample(sim: AerSimulator, pubs: list) -> List[Dict[str, int]]:
    return [_pub_counts(r) for r in AerSampler.from_backend(sim).run(pubs).result()]


class QuantumExecutor:
    """Quantum Circuit Executor — runs circuits on simulators and real devices.

    Args:
        config_file: config path, read with qrisk.config.load_config (ignored
            when ``config`` is given).
        backend_name: overrides the backend named in the config.
        refresh_each_job: reconnect and rebuild the noise model before every
            real-device job (the default). Set False to keep one
            connection and one calibration snapshot for a whole experiment.
        budget: optional QPUBudget; every real-device job is checked and logged.
        hardware: "ibm" submits to IBM Quantum; "emulate" never touches the
            network and replaces the device by a noisy simulator with an
            optional planted fault (for dry runs and pipeline tests).
        emulate_fault: {"gate": "cz", "qubits": [a, b], "p": 0.05} adds extra
            depolarizing error on that gate/qubits in emulated "hardware" only.
        config: pre-loaded config dict.
    """

    def __init__(self, config_file=CONFIG_FILE, *,
                 backend_name: Optional[str] = None,
                 refresh_each_job: bool = True,
                 budget: Optional[QPUBudget] = None,
                 hardware: str = "ibm",
                 emulate_fault: Optional[Dict[str, Any]] = None,
                 config: Optional[Dict[str, Any]] = None):
        if config is None:
            config = load_config(config_file)
        self.config = config
        self.refresh_each_job = bool(refresh_each_job)
        self.budget = budget
        self.hardware = hardware
        self.emulate_fault = emulate_fault
        self._session = None
        self.last_job: Dict[str, Any] = {}

        if hardware == "emulate":
            self.service_manager = None
            self.backend = _fake_backend(backend_name or config["ibm_quantum"].get("backend", "ibm_fez"))
            self._backend_label = backend_name or config["ibm_quantum"].get("backend")
            self.hw_sim = self._build_emulated_hardware()
        elif hardware == "ibm":
            self.service_manager = QuantumServiceManager(config)
            if not self.service_manager.connect():
                raise RuntimeError("Failed to connect to IBM Quantum service")
            self.backend = self.service_manager.select_backend(backend_name)
            if self.backend is None:
                raise RuntimeError(f"Failed to select backend {backend_name}")
            self._backend_label = None
            self._pinned_backend_name = backend_name
        else:
            raise ValueError(f"Unknown hardware mode: {hardware}")

        self.ideal_sim = AerSimulator()
        self.noisy_sim = AerSimulator.from_backend(self.backend)

    # ---------- helpers ----------

    @property
    def _shots(self) -> int:
        return self.config["execution"]["shots"]

    @property
    def _backend_name(self) -> Optional[str]:
        if self._backend_label:
            return self._backend_label
        return getattr(self.backend, "name", None) if self.backend else None

    def _build_emulated_hardware(self) -> AerSimulator:
        from qiskit_aer.noise import NoiseModel, depolarizing_error
        nm = NoiseModel.from_backend(self.backend)
        if self.emulate_fault:
            gate = self.emulate_fault.get("gate", "cz")
            qubits = list(self.emulate_fault["qubits"])
            p = float(self.emulate_fault.get("p", 0.05))
            err = depolarizing_error(p, len(qubits))
            # Planted fault on both orientations of a symmetric two-qubit gate.
            orientations = [qubits, qubits[::-1]] if len(qubits) == 2 else [qubits]
            for q in orientations:
                nm.add_quantum_error(err, gate, q, warnings=False)
        sim = AerSimulator.from_backend(self.backend)
        sim.set_options(noise_model=nm)
        return sim

    def calibration_info(self) -> Dict[str, Any]:
        """Timestamp of the calibration snapshot used for the noisy simulator."""
        info: Dict[str, Any] = {"backend": self._backend_name, "hardware": self.hardware}
        try:
            props = self.backend.properties()
            if props is not None and getattr(props, "last_update_date", None):
                info["calibration_last_update"] = props.last_update_date.isoformat()
        except Exception:
            pass
        return info

    @staticmethod
    def _make_pub(isa_circuit: QuantumCircuit, shots: int):
        return (isa_circuit, [0.0] * len(isa_circuit.parameters), shots)

    def _refresh_runtime_account(self) -> bool:
        """Re-select account/backend before each real-device submission."""
        if not self.service_manager.connect():
            return False
        backend = self.service_manager.select_backend(self._pinned_backend_name)
        if backend is None:
            return False
        self.backend = backend
        self.noisy_sim = AerSimulator.from_backend(self.backend)
        return True

    def refresh_calibration(self) -> None:
        """Re-fetch the backend and rebuild the noisy simulator from its
        latest calibration (call once per DDMin run / batch)."""
        if self.hardware != "ibm":
            return
        try:
            self.backend = self.service_manager.service.backend(self._backend_name)
            self.noisy_sim = AerSimulator.from_backend(self.backend)
        except Exception as e:
            print(f"  (calibration refresh failed, keeping previous snapshot: {e})")

    # ---------- sessions ----------

    def open_session(self, max_time: Optional[str] = None) -> bool:
        """Open a runtime Session (paid plans only). Falls back silently to job mode."""
        if self.hardware != "ibm":
            return False
        try:
            from qiskit_ibm_runtime import Session
            self._session = Session(backend=self.backend, max_time=max_time)
            print(f"Opened runtime session on {self._backend_name}")
            return True
        except Exception as e:
            print(f"Session unavailable ({e}); submitting individual jobs instead.")
            self._session = None
            return False

    def close_session(self) -> None:
        if self._session is not None:
            try:
                self._session.close()
            except Exception:
                pass
            self._session = None

    # ---------- compilation ----------

    def transpile(self, circuit: QuantumCircuit) -> QuantumCircuit:
        """Transpile a circuit to ISA using config optimization_level."""
        opt_level = self.config["execution"]["optimization_level"]
        pm = generate_preset_pass_manager(optimization_level=opt_level, backend=self.backend)
        return pm.run(circuit)

    # ---------- execution ----------

    def _run_real_pubs(self, pubs: list, label: str = "") -> List[Dict[str, int]]:
        """Submit pubs as ONE real-device job and return counts per pub.

        Budget-checked before submission (BudgetExceeded propagates) and
        logged after completion.
        """
        n = len(pubs)
        shots = pubs[0][2] if pubs else None
        reservation = 0.0
        if self.budget is not None:
            reservation = self.budget.check(n_circuits=n, label=label, reserve=True)

        if self.hardware == "emulate":
            counts = _sample(self.hw_sim, pubs)
            self.last_job = {"job_id": None, "seconds": EMULATED_SECONDS_PER_CIRCUIT * n, "measured": False}
            if self.budget is not None:
                self.budget.record(EMULATED_SECONDS_PER_CIRCUIT * n, n, self._backend_name, None,
                                   label=label, measured=True, shots=shots, reservation=reservation)
            return counts

        try:
            if self.refresh_each_job and self._session is None:
                if not self._refresh_runtime_account():
                    raise RuntimeError("Failed to refresh runtime account/backend")
            sampler = RuntimeSampler(mode=self._session or self.backend)
            job = sampler.run(pubs)
        except Exception:
            if self.budget is not None:  # nothing was submitted: release the reservation
                self.budget.record(0.0, 0, self._backend_name, None, label=f"{label} (submit failed)",
                                   measured=True, shots=shots, reservation=reservation)
            raise
        job_id = job.job_id() if hasattr(job, "job_id") else None
        try:
            result = job.result()
        finally:
            seconds, measured = job_usage_seconds(job)
            if seconds is None and self.budget is not None:
                # Could not read usage: charge the pessimistic estimate.
                seconds = self.budget.seconds_per_circuit_estimate() * n
            if self.budget is not None:
                self.budget.record(seconds, n, self._backend_name, job_id,
                                   label=label, measured=measured, shots=shots, reservation=reservation)
            self.last_job = {"job_id": job_id, "seconds": seconds, "measured": measured}
        return [_pub_counts(r) for r in result]

    def run_real_batch(self, circuits: Sequence[QuantumCircuit], shots: Optional[int] = None,
                       label: str = "") -> List[Dict[str, int]]:
        """Run many circuits on the real device as a single job."""
        shots = shots or self._shots
        return self._run_real_pubs([self._make_pub(c, shots) for c in circuits], label=label)

    def run_sim_batch(self, circuits: Sequence[QuantumCircuit], execution_type: str,
                      shots: Optional[int] = None) -> List[Dict[str, int]]:
        shots = shots or self._shots
        sim = self.ideal_sim if execution_type == "ideal_simulator" else self.noisy_sim
        return _sample(sim, [self._make_pub(c, shots) for c in circuits])

    def run_circuit(self, isa_circuit: QuantumCircuit, execution_type: str,
                    shots: Optional[int] = None, label: str = "") -> dict:
        """Run a circuit on ideal/noisy simulator or real device."""
        shots = shots or self._shots

        if execution_type in ("ideal_simulator", "noisy_simulator"):
            counts = self.run_sim_batch([isa_circuit], execution_type, shots)[0]
            return {"success": True, "execution_type": execution_type, "backend": self._backend_name,
                    "job_id": None, "counts": counts, "shots": shots}

        elif execution_type == "real_device":
            try:
                counts = self.run_real_batch([isa_circuit], shots, label=label)[0]
            except BudgetExceeded:
                raise
            except Exception as e:
                return {"success": False, "execution_type": "real_device",
                        "backend": self._backend_name, "job_id": self.last_job.get("job_id"),
                        "error": str(e), "shots": shots}
            return {"success": True, "execution_type": "real_device",
                    "backend": self._backend_name, "job_id": self.last_job.get("job_id"),
                    "qpu_seconds": self.last_job.get("seconds"),
                    "counts": counts, "shots": shots}

        else:
            return {"success": False, "error": f"Unknown execution_type: {execution_type}"}
