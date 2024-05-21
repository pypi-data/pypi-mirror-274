from cybertron_framework.orchestrator.abstract_orchestrator import (
    AbstractOrchestrator,
)


class Orchestrator(AbstractOrchestrator):
    """
    Application orchestrator
    """

    def run(self):
        """
        Main method that will execute all the stages of the pipeline.
        (Input, Transformer, Output/Export)
        """
        super().is_initialized()

        self.benchmark.start("total")

        input_data = self._process_input_process()

        transformed_data = self._process_data_transformation(input_data)

        self._process_export_data(transformed_data)

        self.elapsed_total = self.benchmark.end("total")

    def _process_input_process(self):
        """
        In this stage all the Input information will be downloaded.
        """
        self.logger.info("Starting the input process (1/3).")
        self.benchmark.start("input")
        input_data = {}

        for i, input_manager_id in enumerate(self.input_manager):
            self.logger.info(
                f"-- Input manager {input_manager_id} ({i + 1}/{len(self.input_manager)})."  # noqa: E501
            )
            input_manager = self.input_manager[input_manager_id]
            input_data[input_manager.get_id()] = input_manager.get_data()

        self.elapsed_input = self.benchmark.end("input")
        self.logger.info("Finished the input process.")

        return input_data

    def _process_data_transformation(self, input_data: dict):
        """
        In this stage, all the information downloaded into the Input
        is transformed and a new list of data is generated.
        """
        self.logger.info("Starting the transformation process (2/3).")
        self.benchmark.start("transform")
        transformed_data = {}

        for i, transformer_manager_id in enumerate(self.transformer_manager):
            self.logger.info(
                f"-- Transformer manager {transformer_manager_id} ({i + 1}/{len(self.transformer_manager)})."  # noqa: E501
            )
            transformer_manager = self.transformer_manager[
                transformer_manager_id
            ]

            transformed_data[
                transformer_manager.get_id()
            ] = transformer_manager.transform(
                input_data[transformer_manager_id]
            )

        self.elapsed_transform = self.benchmark.end("transform")
        self.logger.info("Finished the transformation process.")

        return transformed_data

    def _process_export_data(self, transformed_data: dict):
        self.logger.info("Starting the output process (3/3).")
        self.benchmark.start("output")

        for i, output_manager_id in enumerate(self.output_manager):
            self.logger.info(
                f"-- Output manager {output_manager_id} ({i + 1}/{len(self.output_manager)})."  # noqa: E501
            )
            output_manager = self.output_manager[output_manager_id]

            output_manager.put(transformed_data[output_manager_id])

        self.elapsed_output = self.benchmark.end("output")
        self.logger.info("Finished the output process.")

    def get_summary(self):
        return {
            "elapsed_total": self.elapsed_total,
            "elapsed_input": self.elapsed_input,
            "elapsed_transform": self.elapsed_transform,
            "elapsed_output": self.elapsed_output,
        }
