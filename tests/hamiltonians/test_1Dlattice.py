"""Tests for generator analysis."""

from unittest import TestCase

from qiskit.circuit.library import EfficientSU2
from qiskit.pulse import num_qubits
from qiskit.quantum_info.states.statevector import SparsePauliOp

from windsurfer.hamiltonians.oneDlattice import lattice_hamiltonian


class TestPrototypeTemplate(TestCase):
    """Tests prototype template."""

    def test_pair_hamiltonian(self):
        """Tests template class."""
        ha = lattice_hamiltonian(4, [("XX", 1)], False)
        hb = SparsePauliOp.from_sparse_list(
            [
                ("XX", (0, 1), 1),
                ("XX", (1, 2), 1),
                ("XX", (2, 3), 1),
            ],
            num_qubits=4,
        )
        self.assertTrue(ha.equiv(hb))

    def test_pair_hamiltonian_cyclic(self):
        """Tests template class."""
        ha = lattice_hamiltonian(4, [("XX", 1)], True)
        hb = SparsePauliOp.from_sparse_list(
            [
                ("XX", (0, 1), 1),
                ("XX", (1, 2), 1),
                ("XX", (2, 3), 1),
                ("XX", (0, 3), 1),
            ],
            num_qubits=4,
        )
        self.assertTrue(ha.equiv(hb))

    def test_odd_hamiltonian(self):
        """Tests template class."""
        ha = lattice_hamiltonian(5, [("XX", 1)], False)
        hb = SparsePauliOp.from_sparse_list(
            [
                ("XX", (0, 1), 1),
                ("XX", (1, 2), 1),
                ("XX", (2, 3), 1),
                ("XX", (3, 4), 1),
            ],
            num_qubits=5,
        )
        self.assertTrue(ha.equiv(hb))

    def test_odd_hamiltonian_cyclic(self):
        """Tests template class."""
        ha = lattice_hamiltonian(5, [("XX", 1)], True)
        hb = SparsePauliOp.from_sparse_list(
            [
                ("XX", (0, 1), 1),
                ("XX", (1, 2), 1),
                ("XX", (2, 3), 1),
                ("XX", (3, 4), 1),
                ("XX", (0, 4), 1),
            ],
            num_qubits=5,
        )
        self.assertTrue(ha.equiv(hb))
