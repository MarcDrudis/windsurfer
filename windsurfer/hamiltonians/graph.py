import matplotlib.pyplot as plt
from qiskit.quantum_info import SparsePauliOp
from qiskit_nature.second_q.hamiltonians.lattices import (BoundaryCondition,
                                                          KagomeLattice)
from rustworkx import (PyGraph, bipartite_layout, shell_layout, spiral_layout,
                       spring_layout)
from rustworkx.generators import hexagonal_lattice_graph, star_graph
from rustworkx.visualization import mpl_draw


def kagome_lattice_hamiltonian(
    x_dim: int, y_dim: int
) -> tuple[int, SparsePauliOp, KagomeLattice]:
    """
    Returns a weird version of the Kagome lattice for a Heisenberg Hamiltonian
    """
    kagome = kagome_lattice(x_dim, y_dim)
    terms = lambda pauli: [(pauli, (a, b), 1) for a, b in kagome.edge_list()]
    H = SparsePauliOp.from_sparse_list(
        terms("XX") + terms("YY") + terms("ZZ"), num_qubits=kagome.num_nodes()
    )
    return H.num_qubits, H, kagome


def kagome_lattice(x_dim: int, y_dim: int) -> PyGraph:
    """Constructs a Kagome Lattice with x_dim per y_dim stars."""
    # We take a hexagonal lattice as a start.
    # Each node will be converted into a triangle.
    hexagonal = hexagonal_lattice_graph(x_dim, y_dim)
    kagome = PyGraph()
    iterated_nodes = set()

    # For each node in the hexagon we need to add a triangle in our lattice.
    # This triangle must share 1 node with the neighbouring triangles.
    for n_hex in hexagonal.node_indices():
        iterated_nodes.add(n_hex)
        neighbors = hexagonal.neighbors(n_hex)
        triangle = []
        for nn in neighbors:
            # If the neighbor has an existing node that has to be shared
            # with the current triangle, we add it to the current triangle.
            if nn in iterated_nodes:
                existing_node = kagome.find_node_by_weight(nn)
                triangle.append(existing_node)
                kagome[existing_node] = None
            # If the node does not exist yet, we create it and label
            # it to be able to find it later.
            else:
                triangle.append(kagome.add_node(n_hex))

        # We have to add the remaining points in the triangle.
        for _ in range(3 - len(neighbors)):
            triangle.append(kagome.add_node(None))
        assert len(triangle) == 3
        kagome.add_edges_from(
            [(triangle[a], triangle[b], None) for a, b in [(0, 1), (1, 2), (0, 2)]]
        )

    return kagome


if __name__ == "__main__":
    num_qubits, H, kagome = kagome_lattice_hamiltonian(1, 1)
    print(num_qubits)

    mpl_draw(
        kagome,
        with_labels=True,
        pos=spring_layout(kagome, repulsive_exponent=1, adaptive_cooling=True),
    )
    plt.show()
