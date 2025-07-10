from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance
from qiskit import Aer


backend = Aer.get_backend('qasm_simulator')

quantum_instance = QuantumInstance(backend,shots=500)

my_shor = Shor(N=95,a=2,quantum_instance=quantum_instance)

print(Shor.run(my_shor))
