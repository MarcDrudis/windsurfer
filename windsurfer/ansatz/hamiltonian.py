from qiskit.circuit import Parameter, QuantumCircuit
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import Pauli, SparsePauliOp, StabilizerState
from qiskit.synthesis.evolution.product_formula import evolve_pauli


def ansatz_QRTE_Hamiltonian(H: SparsePauliOp | Pauli, reps: int = 1) -> QuantumCircuit:
    qc = QuantumCircuit(H.num_qubits)

    if isinstance(H, SparsePauliOp):
        for i, pauli in enumerate(list(H.paulis) * reps):
            qc.compose(
                evolve_pauli(
                    pauli, time=Parameter(f"θ[{i}]") / 2, cx_structure="chain"
                ),
                inplace=True,
            )
    elif isinstance(H, Pauli):
        qc.compose(
            evolve_pauli(H, time=Parameter(f"θ") / 2, cx_structure="chain"),
            inplace=True,
        )
    else:
        raise ValueError("H has to be either SparsePauliOp or Pauli.")

    return qc


def ansatz_QITE_Hamiltonian(
    H: SparsePauliOp | Pauli, reps: int = 1, prep_circuit: QuantumCircuit = None
) -> QuantumCircuit:
    qc = QuantumCircuit(H.num_qubits) if prep_circuit is None else prep_circuit.copy()
    stabilizers = StabilizerState(qc).clifford.to_labels(mode="S")
    print(stabilizers)

    if isinstance(H, SparsePauliOp):
        for i, term in enumerate(list(H.paulis) * reps):
            pauli = None
            for s in stabilizers:
                if term.anticommutes(s):
                    pauli = term @ Pauli(s)
                    continue

            if pauli is not None:
                qc.compose(
                    evolve_pauli(
                        term, time=Parameter(f"θ[{i}]") / 2, cx_structure="chain"
                    ),
                    inplace=True,
                )
            else:
                print(f"We did not find a Pauli for {term}")
    # elif isinstance(H, Pauli):
    #     qc.compose(
    #         evolve_pauli(H, time=Parameter(f"θ") / 2, cx_structure="chain"),
    #         inplace=True,
    #     )
    else:
        raise ValueError("H has to be either SparsePauliOp or Pauli.")

    return qc


if __name__ == "__main__":
    import numpy as np

    H = SparsePauliOp.from_sparse_list(
        [("XZ", [2, 1], 1.3), ("Z", [-1], 1.9), ("XX", [0, 1], 1.3)], num_qubits=4
    )
    qc = ansatz_QITE_Hamiltonian(H)
    print(qc.decompose())
    print(qc)
    # print(
    #     StabilizerState(qc.assign_parameters(np.zeros(qc.num_parameters))).clifford[
    #         "Stabilizer"
    #     ]
    # )
