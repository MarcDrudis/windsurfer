import numpy as np
from qiskit.quantum_info import SparsePauliOp


def _n_local_connections(num_qubits: int, term: str, periodic: bool):
    if periodic:
        connections = [
            np.arange(i, i + len(term)) % num_qubits for i in range(num_qubits)
        ]
    else:
        connections = [
            np.arange(i, i + len(term)) for i in range(num_qubits - len(term) + 1)
        ]
    return connections


def lattice_hamiltonian(
    num_qubits: int,
    terms: list[tuple[str, float]],
    periodic: bool = False,
):
    """
    Returns a Hamiltonian in a 1D lattice.
    Args:
    num_qubits: Number of qubits in the system.
    terms:Terms to be repited over the lattice.
    periodic: If true, use periodic boundary conditions
    """

    all_terms_list = []
    for term, coeff in terms:
        all_terms_list += [
            (term, c, coeff) for c in _n_local_connections(num_qubits, term, periodic)
        ]

    H = SparsePauliOp.from_sparse_list(all_terms_list, num_qubits=num_qubits)

    return H


if __name__ == "__main__":
    print(lattice_hamiltonian(5, terms=[("XX", 1)], periodic=True))
    print(lattice_hamiltonian(5, terms=[("XIX", 1)], periodic=True))
    print(lattice_hamiltonian(5, terms=[("XIX", 1)], periodic=False))
