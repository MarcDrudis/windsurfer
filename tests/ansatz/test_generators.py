"""Tests for generator analysis."""

from unittest import TestCase

import numpy as np
from qiskit.circuit.library import EfficientSU2
from qiskit.pulse import num_qubits
from qiskit.quantum_info import Statevector, state_fidelity
from qiskit.quantum_info.states.statevector import SparsePauliOp

from windsurfer.ansatz.generators import (circuit_from_generators, get_paulis,
                                          one_pass)


class TestHamiltonians(TestCase):
    """Tests if we can get the generators out of any circuit."""

    def test_pair_hamiltonian(self):
        """Test if the resulting circuit is indeed equivalent."""

        qc = EfficientSU2(5).decompose()

        gates, entanglement_mask, parameters = get_paulis(qc)

        entanglement, generators = one_pass(gates, entanglement_mask)

        newqc = circuit_from_generators(generators, parameters)

        for n in range(15):
            parameters = np.random.uniform(-1, 1, qc.num_parameters)
            self.assertTrue(
                np.isclose(
                    1,
                    state_fidelity(
                        Statevector(qc.assign_parameters(parameters)),
                        Statevector(newqc.assign_parameters(parameters / 2)),
                    ),
                )
            )
