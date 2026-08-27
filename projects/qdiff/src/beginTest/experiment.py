
from qiskit import IBMQ, execute
from qiskit import QuantumCircuit
from qiskit.providers.aer import QasmSimulator
from qiskit.tools.visualization import plot_histogram
from qiskit.test.mock import FakeSantiago
from qiskit.test.mock import FakeAthens

if __name__ == '__main__':
    #device_backend = FakeVigo()
    device_backend = FakeAthens()
    vigo_simulator = QasmSimulator.from_backend(device_backend)

    print(isinstance(1,int))
    print(tuple([1]))
    print(device_backend.properties().gate_error(gate="cx",qubits=(0,1)))
    print(device_backend.properties().gate_error(gate="cx", qubits=(4, 3)))
    print(device_backend.properties().gate_error(gate="cx", qubits=(1, 2)))
    print(device_backend.properties().gate_error(gate="cx", qubits=(2, 3)))
    print(device_backend.properties().gate_error(gate="u2",qubits=2))
    print(device_backend.properties().gate_error(gate="u2", qubits=1))
    print(device_backend.properties().gate_error(gate="u2", qubits=0))
    print(device_backend.properties().gate_error(gate="u2", qubits=3))
