import unittest
from unittest.mock import MagicMock

from cybertron_framework.input.input_manager_interface import IInputManager
from cybertron_framework.orchestrator.types.sequence import (
    SequenceOrchestrator,
)
from cybertron_framework.output.output_manager_interface import IOutputManager
from cybertron_framework.transformer.transformer_manager_interface import (
    ITransformerManager,
)


def mock_first_input_success():
    mock_input_manager = MagicMock(spec=IInputManager)

    input_data = [{"pipeline_unique_id": "input_data"}]
    mock_input_manager.get_data.return_value = input_data

    return mock_input_manager


def mock_second_input_success():
    mock_input_manager = MagicMock(spec=IInputManager)

    input_data = [{"pipeline_unique_id2": "input_data2"}]
    mock_input_manager.get_data.return_value = input_data

    return mock_input_manager


def mock_first_transform_success():
    mock_transformer_manager = MagicMock(spec=ITransformerManager)
    transformed_data = [{"pipeline_unique_id": "transformed_data"}]
    mock_transformer_manager.transform.return_value = transformed_data

    return mock_transformer_manager


def mock_second_transform_success():
    mock_transformer_manager = MagicMock(spec=ITransformerManager)
    transformed_data = [{"pipeline_unique_id2": "transformed_data2"}]
    mock_transformer_manager.transform.return_value = transformed_data

    return mock_transformer_manager


def mock_thrid_transform_success():
    mock_transformer_manager = MagicMock(spec=ITransformerManager)
    transformed_data = [
        {"pipeline_unique_id": "transformed_data"},
        {"pipeline_unique_id2": "transformed_data2"},
    ]
    mock_transformer_manager.transform.return_value = transformed_data

    return mock_transformer_manager


def mock_first_output_success():
    mock_output_manager = MagicMock(spec=IOutputManager)

    return mock_output_manager


class TestDynamicOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = SequenceOrchestrator()
        self.mock_input_manager = mock_first_input_success()
        self.mock_transformer_manager = mock_first_transform_success()
        self.mock_output_manager = mock_first_output_success()

        self.pipeline_steps = [
            {
                "id": "input1",
                "type": "input",
                "manager": self.mock_input_manager,
            },
            {
                "id": "transformer1",
                "type": "transformer",
                "manager": self.mock_transformer_manager,
                "inputs": ["input1"],
            },
            {
                "id": "output1",
                "type": "output",
                "manager": self.mock_output_manager,
                "inputs": ["transformer1"],
            },
        ]

    def test_sequence_orquestrator_run_each_step_with_correct_oarams(self):
        orchestrator = SequenceOrchestrator()

        orchestrator.run(self.pipeline_steps)

        self.mock_input_manager.get_data.assert_called_with()
        self.mock_transformer_manager.transform.assert_called_with(
            [{"pipeline_unique_id": "input_data"}]
        )
        self.mock_output_manager.put.assert_called_with(
            [{"pipeline_unique_id": "transformed_data"}]
        )

    def test_sequence_orquestrator_run_each_step_with_multiple_steps_dependencies(  # noqa: E501
        self,
    ):
        second_input_mock = mock_second_input_success()
        second_transformer_mock = mock_second_transform_success()
        third_transformer_mock = mock_thrid_transform_success()
        orchestrator = SequenceOrchestrator()

        pipeline_steps = [
            {
                "id": "input1",
                "type": "input",
                "manager": self.mock_input_manager,
            },
            {"id": "input2", "type": "input", "manager": second_input_mock},
            {
                "id": "transformer1",
                "type": "transformer",
                "manager": self.mock_transformer_manager,
                "inputs": ["input1"],
            },
            {
                "id": "transformer2",
                "type": "transformer",
                "manager": second_transformer_mock,
                "inputs": ["input2"],
            },
            {
                "id": "transformer3",
                "type": "transformer",
                "manager": third_transformer_mock,
                "inputs": ["transformer1", "transformer2"],
            },
            {
                "id": "output1",
                "type": "output",
                "manager": self.mock_output_manager,
                "inputs": ["transformer3"],
            },
        ]

        orchestrator.run(pipeline_steps)

        self.mock_input_manager.get_data.assert_called_with()
        second_input_mock.get_data.assert_called_with()

        self.mock_transformer_manager.transform.assert_called_with(
            [{"pipeline_unique_id": "input_data"}]
        )
        second_transformer_mock.transform.assert_called_with(
            [{"pipeline_unique_id2": "input_data2"}]
        )
        third_transformer_mock.transform.assert_called_with(
            [{"pipeline_unique_id": "transformed_data"}],
            [{"pipeline_unique_id2": "transformed_data2"}],
        )

        self.mock_output_manager.put.assert_called_with(
            [
                {"pipeline_unique_id": "transformed_data"},
                {"pipeline_unique_id2": "transformed_data2"},
            ]
        )
