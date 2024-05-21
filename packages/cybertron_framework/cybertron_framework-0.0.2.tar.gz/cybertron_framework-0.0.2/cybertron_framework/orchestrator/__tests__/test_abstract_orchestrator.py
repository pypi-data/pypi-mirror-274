import unittest
from unittest.mock import MagicMock

from cybertron_framework.orchestrator.abstract_orchestrator import (
    AbstractOrchestrator,
    IInputManager,
    IOutputManager,
    ITransformerManager,
)


class TestAbstractOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = AbstractOrchestrator()

    def test_is_initialized_raises_exception_when_mapper_manager_is_not_defined(  # noqa: E501
        self,
    ):
        with self.assertRaises(RuntimeError):
            self.orchestrator.is_initialized()

    def test_is_initialized_raises_exception_when_input_manager_is_not_defined(
        self,
    ):
        self.orchestrator.mapper_manager = MagicMock()
        with self.assertRaises(RuntimeError):
            self.orchestrator.is_initialized()

    def test_is_initialized_raises_exception_when_transformer_manager_is_not_defined(  # noqa: E501
        self,
    ):
        self.orchestrator.mapper_manager = MagicMock()
        self.orchestrator.input_manager = MagicMock()
        with self.assertRaises(RuntimeError):
            self.orchestrator.is_initialized()

    def test_is_initialized_raises_exception_when_output_manager_is_not_defined(  # noqa: E501
        self,
    ):
        self.orchestrator.mapper_manager = MagicMock()
        self.orchestrator.input_manager = MagicMock()
        self.orchestrator.transformer_manager = MagicMock()

        with self.assertRaises(RuntimeError):
            self.orchestrator.is_initialized()

    def test_set_input_manager_adds_input_manager_correctly(self):
        input_manager_mock = MagicMock(spec=IInputManager)
        input_manager_mock.get_id.return_value = "test_input_manager"

        self.orchestrator.set_input_manager(input_manager_mock)

        self.assertIn("test_input_manager", self.orchestrator.input_manager)
        self.assertEqual(
            self.orchestrator.input_manager["test_input_manager"],
            input_manager_mock,
        )

    def test_set_transformer_manager_adds_transformer_manager_correctly(self):
        transformer_manager_mock = MagicMock(spec=ITransformerManager)
        transformer_manager_mock.get_id.return_value = (
            "test_transformer_manager"
        )

        self.orchestrator.set_transformer_manager(transformer_manager_mock)

        self.assertIn(
            "test_transformer_manager", self.orchestrator.transformer_manager
        )
        self.assertEqual(
            self.orchestrator.transformer_manager["test_transformer_manager"],
            transformer_manager_mock,
        )

    def test_set_output_manager_adds_output_manager_correctly(self):
        output_manager_mock = MagicMock(spec=IOutputManager)
        output_manager_mock.get_id.return_value = "test_output_manager"

        self.orchestrator.set_output_manager(output_manager_mock)

        self.assertIn("test_output_manager", self.orchestrator.output_manager)
        self.assertEqual(
            self.orchestrator.output_manager["test_output_manager"],
            output_manager_mock,
        )
