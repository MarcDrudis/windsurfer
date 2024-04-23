from qiskit.circuit import Parameter, QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Pauli, SparsePauliOp


def get_paulis(
    qc: QuantumCircuit,
) -> tuple[list[SparsePauliOp], list[bool], list[Parameter]]:
    """
    Returns a tuple with a list of a decomposition of all gates into sparse pauli operators,
    a mask that encodes the position of entangling gates without parameter, and a list of,
    the parameters in order for the rest of the gates.
    """
    gates = list()
    entanglement_mask = list()
    parameters = list()
    simple_generators = {"rx": "X", "ry": "Y", "rz": "Z"}
    entanglement_gates = {"cx"}
    for instruction in qc:
        name = instruction.operation.name
        parameter = instruction.operation.params
        registers = [q._index for q in instruction.qubits]
        isEntanglement = None
        pauli = None
        if name in simple_generators:
            pauli = SparsePauliOp.from_sparse_list(
                [(simple_generators[name], registers, 1.0)], num_qubits=qc.num_qubits
            )
            isEntanglement = False
        elif name in entanglement_gates:
            pauli = SparsePauliOp.from_sparse_list(
                [
                    ("II", registers, 0.5),
                    ("ZI", registers, 0.5),
                    ("IX", registers, 0.5),
                    ("ZX", registers, -0.5),
                ],
                num_qubits=qc.num_qubits,
            )
            isEntanglement = True
        else:
            print("something went wrong")
            print(name)

        gates.append(pauli)
        entanglement_mask.append(isEntanglement)
        parameters.append(parameter)

    parameters = [p[0] for ent, p in zip(entanglement_mask, parameters) if not ent]
    return gates, entanglement_mask, parameters


def one_pass(gates: list[tuple[SparsePauliOp, bool]], entanglement_mask: list[bool]):
    """
    With the data encoded as Pauli operators, we take the conjugate of each pauli in
    the rotation gates with each one of the relevant entangling layers so that all the
    entangling layers are placed to the left of the circuit.
    """
    entanglement_indices = [n for n, is_ent in enumerate(entanglement_mask) if is_ent]

    for n in entanglement_indices:
        for m in range(n):
            if m not in entanglement_indices:
                gates[m] = (gates[n] @ gates[m] @ gates[n]).simplify()

    entanglement_gates = [g for n, g in enumerate(gates) if n in entanglement_indices]
    generators = [g for n, g in enumerate(gates) if n not in entanglement_indices]

    return entanglement_gates, generators


def circuit_from_generators(
    generators: list[Pauli], parameters: list[Parameter]
) -> list[QuantumCircuit]:
    """
    Creates a circuit from a list of generators and parameters.
    """
    qc = QuantumCircuit(generators[0].num_qubits)
    for g, p in zip(generators, parameters):
        qc.compose(
            PauliEvolutionGate(g, time=p),
            inplace=True,
        )
    return qc


#
#
# print(instructions)
#
# xo = SparsePauliOp.from_sparse_list([("X", (0,), 1.0)], num_qubits=2)
# cx = SparsePauliOp.from_sparse_list(
#     [
#         ("II", (0, 1), 0.5),
#         ("ZI", (0, 1), 0.5),
#         ("IX", (0, 1), 0.5),
#         ("ZX", (0, 1), -0.5),
#     ],
#     num_qubits=2,
# )
# print(xo)
# print(cx)
# commuted = (cx @ xo @ cx).simplify()
# print(commuted)
