from qiskit.aqua.algorithms import Shor
from qiskit.aqua import QuantumInstance
import numpy as np
from qiskit import QuantumCircuit,Aer,execute
from qiskit.tools.visualization import plot_histogram
import matplotlib.pyplot as plt

'''
Aer is Qiskit's module that provides simulators to mimic how a quantum computer behaves.
This is a quantum circuit simulator that mimics how real quantum computers would behave when measuring qubits.
It executes circuits multiple times (shots) to collect measurement outcomes (since quantum results are probabilistic).
This line sets up a quantum simulator where we'll "pretend" to run Shor’s algorithm like on a real quantum computer.
'''
backend = Aer.get_backend('qasm_simulator')

'''
creating a QuantumInstance—this is a wrapper that handles:
Backend configuration
Number of shots (how many times to run the circuit)
'''
quantum_instance = QuantumInstance(backend,shots=1000)

'''creating an instance of the Shor class, with these parameters:
N=15 is The number you want to factor.
a=2	is a random integer < N and coprime with N. Shor’s algorithm works by finding the period of a^x mod N.
'''
my_shor = Shor(N=15,a=2,quantum_instance=quantum_instance)

print(Shor.run(my_shor))

def c_amod15(a,power):
    U = QuantumCircuit(4)
    for iteration in range(power):
        U.swap(2,3)
        U.swap(1,2)
        U.swap(0,1)
        for q in range(4):
            U.x(q)
    U=U.to_gate()
    U.name="%i* %i mod 15" %(a,power)
    c_U = U.control()
    return c_U

n_count = 8
a = 7

def qft_dagger(n):
    qc = QuantumCircuit(n)
    for qubit in range(n//2):
        qc.swap(qubit,n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cul(-np.pi/float(2**(j-m)),m,j)
        qc.h(j)
        qc.name="QFT Dagger"
        return qc
    
qc = QuantumCircuit(n_count+4,n_count)
    
for q in range(n_count):
    qc.h(q)
    
qc.x(3+n_count)
    
for q in range(n_count):
    qc.append(c_amod15(a,2**q),[q]+[i+n_count for i in range(4)])
        
qc.append(qft_dagger(n_count),range(n_count))
qc.measure(range(n_count),range(n_count))
print(qc.draw('text'))

backend = Aer.get_backend('qasm_simulator')
results = execute(qc,backend,shots=2048).result()
counts = results.get_counts()
plot_histogram(counts)
plt.show()

