from __future__ import annotations
from typing import Dict, Optional, Sequence
import json

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_ibm_runtime import SamplerV2 as RuntimeSampler

from .runtime_ops import QuantumServiceManager


class QuantumExecutor:
    """Quantum Circuit Executor — runs circuits on simulators and real devices."""

    def __init__(self, config_file="quantum_config.json"):
        with open(config_file, "r") as f:
            self.config = json.load(f)
        self.service_manager = QuantumServiceManager(config_file=config_file)
        assert self.service_manager.connect(), "Failed to connect to IBM Quantum service"
        self.backend = self.service_manager.select_backend()
        assert self.backend is not None, "Failed to select backend"

        self.ideal_sim = AerSimulator()
        self.noisy_sim = AerSimulator.from_backend(self.backend)
        self._job_service_by_id: Dict[str, object] = {}

    @property
    def _shots(self) -> int:
        return self.config["execution"]["shots"]

    @property
    def _backend_name(self) -> Optional[str]:
        return getattr(self.backend, "name", None) if self.backend else None

    @staticmethod
    def _extract_counts(result) -> Dict[str, int]:
        """Extract counts from PrimitiveResult via DataBin -> BitArray.get_counts()."""
        data = result[0].data
        for bit_array in data.values():
            if hasattr(bit_array, "get_counts"):
                return bit_array.get_counts()
        return {}

    def _make_pub(self, isa_circuit: QuantumCircuit, shots: int,
                  param_vals: Optional[Sequence[float]] = None):
        params = [] if not isa_circuit.parameters else (param_vals or [0.0] * len(isa_circuit.parameters))
        return (isa_circuit, params, shots)

    def _refresh_runtime_account(self) -> bool:
        """Re-select account/backend before each real-device submission."""
        if not self.service_manager.connect():
            return False
        backend = self.service_manager.select_backend()
        if backend is None:
            return False
        self.backend = backend
        self.noisy_sim = AerSimulator.from_backend(self.backend)
        return True

    def transpile(self, circuit: QuantumCircuit) -> QuantumCircuit:
        """Transpile a circuit to ISA using config optimization_level."""
        opt_level = self.config["execution"]["optimization_level"]
        pm = generate_preset_pass_manager(optimization_level=opt_level, backend=self.backend)
        return pm.run(circuit)

    def run_circuit(self, isa_circuit: Optional[QuantumCircuit] = None,
                    execution_type: Optional[str] = None,
                    shots: Optional[int] = None,
                    param_vals: Optional[Sequence[float]] = None) -> dict:
        """Run a circuit on ideal/noisy simulator or real device."""
        if execution_type is None:
            raise RuntimeError("execution_type is required")
        if isa_circuit is None:
            raise RuntimeError("ISA circuit is required")
        shots = shots or self._shots
        pub = self._make_pub(isa_circuit, shots, param_vals)

        if execution_type in ("ideal_simulator", "noisy_simulator"):
            sim = self.ideal_sim if execution_type == "ideal_simulator" else self.noisy_sim
            sampler = AerSampler.from_backend(sim)
            counts = self._extract_counts(sampler.run([pub]).result())
            return {"success": True, "execution_type": execution_type, "backend": self._backend_name,
                    "job_id": None, "counts": counts, "shots": shots}

        elif execution_type == "real_device":
            if not self._refresh_runtime_account():
                return {"success": False, "execution_type": "real_device",
                        "backend": self._backend_name, "job_id": None,
                        "error": "Failed to refresh runtime account/backend", "shots": shots}
            sampler = RuntimeSampler(mode=self.backend)
            job = sampler.run([pub])
            job_id = job.job_id() if hasattr(job, "job_id") else None
            if job_id:
                self._job_service_by_id[job_id] = self.service_manager.service
            try:
                counts = self._extract_counts(job.result())
            except Exception as e:
                return {"success": False, "execution_type": "real_device",
                        "backend": self._backend_name, "job_id": job_id,
                        "error": str(e), "shots": shots}
            return {"success": True, "execution_type": "real_device",
                    "backend": self._backend_name, "job_id": job_id,
                    "counts": counts, "shots": shots}

        else:
            return {"success": False, "error": f"Unknown execution_type: {execution_type}"}
