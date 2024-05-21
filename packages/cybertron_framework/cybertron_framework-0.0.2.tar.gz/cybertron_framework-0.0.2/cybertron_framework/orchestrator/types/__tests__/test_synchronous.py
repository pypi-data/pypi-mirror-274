import unittest
from unittest.mock import MagicMock

from cybertron_framework.input.input_manager_interface import IInputManager
from cybertron_framework.orchestrator.types.synchronous import Orchestrator
from cybertron_framework.output.output_manager_interface import IOutputManager
from cybertron_framework.transformer.transformer_manager_interface import (
    ITransformerManager,
)


class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = Orchestrator()
        self.mock_input_manager = MagicMock(spec=IInputManager)
        self.mock_transformer_manager = MagicMock(spec=ITransformerManager)
        self.mock_output_manager = MagicMock(spec=IOutputManager)

    def test_run_executes_all_stages_of_pipeline(self):
        # Mocking input data
        input_data = {"pipeline_unique_id": "input_data"}
        self.mock_input_manager.get_id.return_value = "pipeline_unique_id"
        self.mock_input_manager.get_data.return_value = input_data

        # Mocking transformed data
        transformed_data = {"pipeline_unique_id": "transformed_data"}
        self.mock_transformer_manager.get_id.return_value = (
            "pipeline_unique_id"
        )
        self.mock_transformer_manager.transform.return_value = transformed_data

        # Mocking output data
        self.mock_output_manager.get_id.return_value = "pipeline_unique_id"

        # Setting up orchestrator
        self.orchestrator.set_input_manager(self.mock_input_manager)
        self.orchestrator.set_transformer_manager(
            self.mock_transformer_manager
        )
        self.orchestrator.set_output_manager(self.mock_output_manager)

        # Running the orchestrator
        self.orchestrator.run()

        self.mock_input_manager.get_data.assert_called_once()
        self.mock_transformer_manager.transform.assert_called_once_with(
            {"pipeline_unique_id": "input_data"}
        )
        self.mock_output_manager.put.assert_called_once_with(
            {"pipeline_unique_id": "transformed_data"}
        )

    def test_get_summary_returns_correct_summary(self):
        self.orchestrator.elapsed_total = 10
        self.orchestrator.elapsed_input = 2
        self.orchestrator.elapsed_transform = 5
        self.orchestrator.elapsed_output = 3

        summary = self.orchestrator.get_summary()

        self.assertEqual(summary["elapsed_total"], 10)
        self.assertEqual(summary["elapsed_input"], 2)
        self.assertEqual(summary["elapsed_transform"], 5)
        self.assertEqual(summary["elapsed_output"], 3)

    def test_fail_when_input_step_is_missing(self):
        # Mocking transformed data
        transformed_data = {"pipeline_unique_id": "transformed_data"}
        self.mock_transformer_manager.get_id.return_value = (
            "pipeline_unique_id"
        )
        self.mock_transformer_manager.transform.return_value = transformed_data

        # Mocking output data
        self.mock_output_manager.get_id.return_value = "pipeline_unique_id"

        # Setting up orchestrator without input step
        self.orchestrator.set_transformer_manager(
            self.mock_transformer_manager
        )
        self.orchestrator.set_output_manager(self.mock_output_manager)

        with self.assertRaises(RuntimeError):
            self.orchestrator.run()

    def test_fail_when_transformer_step_is_missing(self):
        # Mocking input data
        input_data = {"pipeline_unique_id": "input_data"}
        self.mock_input_manager.get_id.return_value = "pipeline_unique_id"
        self.mock_input_manager.get_data.return_value = input_data

        # Mocking output data
        self.mock_output_manager.get_id.return_value = "pipeline_unique_id"

        # Setting up orchestrator without transformer
        self.orchestrator.set_input_manager(self.mock_input_manager)
        self.orchestrator.set_output_manager(self.mock_output_manager)

        with self.assertRaises(RuntimeError):
            self.orchestrator.run()

    def test_fail_when_output_step_is_missing(self):
        # Mocking input data
        input_data = {"pipeline_unique_id": "input_data"}
        self.mock_input_manager.get_id.return_value = "pipeline_unique_id"
        self.mock_input_manager.get_data.return_value = input_data

        # Mocking transformed data
        transformed_data = {"pipeline_unique_id": "transformed_data"}
        self.mock_transformer_manager.get_id.return_value = (
            "pipeline_unique_id"
        )
        self.mock_transformer_manager.transform.return_value = transformed_data

        # Setting up orchestrator without output
        self.orchestrator.set_input_manager(self.mock_input_manager)
        self.orchestrator.set_transformer_manager(
            self.mock_transformer_manager
        )

        with self.assertRaises(RuntimeError):
            self.orchestrator.run()

    def test_fail_when_step_input_has_not_get_data_method(self):
        # Mocking input data
        self.mock_input_manager.get_id.return_value = "pipeline_unique_id"
        self.mock_input_manager.get_data.side_effect = AttributeError(
            "Mock has no attribute 'get_data'"
        )

        # Mocking transformed data
        transformed_data = {"pipeline_unique_id": "transformed_data"}
        self.mock_transformer_manager.get_id.return_value = (
            "pipeline_unique_id"
        )
        self.mock_transformer_manager.transform.return_value = transformed_data

        # Mocking output data
        self.mock_output_manager.get_id.return_value = "pipeline_unique_id"

        # Setting up orchestrator
        self.orchestrator.set_input_manager(self.mock_input_manager)
        self.orchestrator.set_transformer_manager(
            self.mock_transformer_manager
        )
        self.orchestrator.set_output_manager(self.mock_output_manager)

        with self.assertRaises(AttributeError):
            self.orchestrator.run()
