from cybertron_framework.helper.benchmark import Benchmark
from cybertron_framework.helper.logger import Logger
from cybertron_framework.input.input_manager_interface import IInputManager
from cybertron_framework.orchestrator.orchestrator_interface import (  # noqa: E501
    IOrchestrator,
)
from cybertron_framework.output.output_manager_interface import IOutputManager
from cybertron_framework.transformer.transformer_manager_interface import (
    ITransformerManager,
)


class AbstractOrchestrator(IOrchestrator):
    """
    Abstract application orchestrator
    """

    def __init__(self):
        self.mapper_manager = None
        self.input_manager = None
        self.transformer_manager = None
        self.output_manager = None
        self.benchmark = Benchmark()
        self.logger = Logger()
        self.elapsed_total = 0
        self.elapsed_input = 0
        self.elapsed_transform = 0
        self.elapsed_output = 0

    def is_initialized(self):
        if self.input_manager is None:
            raise RuntimeError("No InputManager defined.")
        if self.transformer_manager is None:
            raise RuntimeError("No TransformerManager defined.")
        if self.output_manager is None:
            raise RuntimeError("No OutputManager defined.")

    def set_input_manager(self, input_manager):
        if not isinstance(input_manager, IInputManager):
            raise TypeError(
                "The provided InputManager does not implement the IInputManager interface."  # noqa: E501
            )

        if self.input_manager is None:
            self.input_manager = {}

        self.input_manager[input_manager.get_id()] = input_manager

    def set_transformer_manager(self, transformer_manager):
        if not isinstance(transformer_manager, ITransformerManager):
            raise TypeError(
                "The provided TransformerManager does not implement the ITransformerManager interface."  # noqa: E501
            )

        if self.transformer_manager is None:
            self.transformer_manager = {}

        self.transformer_manager[
            transformer_manager.get_id()
        ] = transformer_manager

    def set_output_manager(self, output_manager):
        if not isinstance(output_manager, IOutputManager):
            raise TypeError(
                "The provided OutputManager does not implement the IOutputManager interface."  # noqa: E501
            )

        if self.output_manager is None:
            self.output_manager = {}

        self.output_manager[output_manager.get_id()] = output_manager
