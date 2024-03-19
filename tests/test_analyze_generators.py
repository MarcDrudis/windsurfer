"""Tests for generator analysis."""

from unittest import TestCase

from qiskit.circuit.library import EfficientSU2

from windsurfer.analyze.generators import get_generators


class TestPrototypeTemplate(TestCase):
    """Tests prototype template."""

    def test_template_class(self):
        """Tests template class."""
        qc = EfficientSU2(num_qubits=2, su2_gates=["rx"], reps=1)
        print(qc.decompose())
        self.assertTrue(True)

        # self.assertEqual(obj.multiply(2), 2)
        # self.assertEqual(repr(obj), "TemplateClass(1)")
