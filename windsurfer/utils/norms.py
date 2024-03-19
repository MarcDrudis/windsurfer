from qiskit.quantum_info import SparsePauliOp
from scipy.sparse.linalg import eigsh


def eigenrange(H: SparsePauliOp) -> float:
    if isinstance(H, SparsePauliOp):
        H = H.to_matrix(sparse=True)
        smallest = eigsh(H, which="SA", k=1)[0][0]
        biggest = eigsh(H, which="LA", k=1)[0][0]
    else:
        raise ValueError(
            "The current Hamiltonian type is not supported. Hamiltonian is", type(H)
        )

    return biggest - smallest
