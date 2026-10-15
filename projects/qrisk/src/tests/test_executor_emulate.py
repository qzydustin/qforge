"""QuantumExecutor end to end in emulate mode: fake ibm_fez + Aer, no network, no tokens."""

import math

import pytest
from qiskit import QuantumCircuit

from qrisk.config import load_config
from qrisk.executor import QuantumExecutor
from qrisk.metrics import calculate_tvd

SHOTS = 1024

# qiskit-ibm-runtime's own transpiler plugin warns about its deprecated fractional-gate translation.
pytestmark = pytest.mark.filterwarnings("ignore:.*IBMFractionalTranslationPlugin:DeprecationWarning")


@pytest.fixture(scope="module")
def executor():
    return QuantumExecutor(config=load_config(example=True), hardware="emulate", backend_name="ibm_fez")


@pytest.fixture(scope="module")
def bell_isa(executor):
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    return executor.transpile(qc)


def test_run_circuit_on_every_target(executor, bell_isa):
    counts = {}
    for target in ("ideal_simulator", "noisy_simulator", "real_device"):
        result = executor.run_circuit(bell_isa, target, shots=SHOTS)
        assert result["success"], result
        assert result["backend"] == "ibm_fez"
        assert sum(result["counts"].values()) == SHOTS
        counts[target] = result["counts"]

    assert set(counts["ideal_simulator"]) <= {"00", "11"}
    for other in ("noisy_simulator", "real_device"):
        tvd, _ = calculate_tvd(counts["ideal_simulator"], counts[other])
        assert math.isfinite(tvd) and 0.0 <= tvd <= 1.0


def test_batches_match_single_runs(executor, bell_isa):
    sims = executor.run_sim_batch([bell_isa, bell_isa], "ideal_simulator", shots=SHOTS)
    real = executor.run_real_batch([bell_isa], shots=SHOTS)
    assert [sum(c.values()) for c in sims + real] == [SHOTS] * 3
    assert executor.last_job["job_id"] is None


def test_load_config_backend_override():
    cfg = load_config(example=True, backend="ibm_marrakesh")
    assert cfg["ibm_quantum"]["backend"] == "ibm_marrakesh"
    assert load_config(example=True)["ibm_quantum"]["backend"] == "ibm_fez"


def test_load_config_reports_bad_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"ibm_quantum": {"backend": "ibm_fez",}}')
    with pytest.raises(ValueError, match="line 1"):
        load_config(bad)
