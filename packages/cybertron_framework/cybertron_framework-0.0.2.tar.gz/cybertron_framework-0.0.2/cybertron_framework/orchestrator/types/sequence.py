import concurrent.futures

from cybertron_framework.orchestrator.abstract_orchestrator import (
    AbstractOrchestrator,
)


class SequenceOrchestrator(AbstractOrchestrator):
    def run(self, pipeline_steps):
        self.benchmark.start("total")

        input_data = self._process_parallel_inputs(pipeline_steps)

        transformer_outputs = self._process_transformers(
            pipeline_steps, input_data
        )

        self._process_output(pipeline_steps, transformer_outputs)

        self.elapsed_total = self.benchmark.end("total")

    def _process_parallel_inputs(self, pipeline_steps):
        self.logger.info("Starting parallel input process (1/3).")
        self.benchmark.start("input")

        input_data = {}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            input_futures = {
                step["id"]: executor.submit(step["manager"].get_data)
                for step in pipeline_steps
                if step["type"] == "input"
            }

        for input_id, future in input_futures.items():
            input_data[input_id] = future.result()

        self.elapsed_input = self.benchmark.end("input")
        self.logger.info("Finished parallel input process.")

        return input_data

    def _process_transformers(self, pipeline_steps, input_data):
        self.logger.info("Starting transformers process (2/3).")
        self.benchmark.start("transform")

        transformer_outputs = {}

        for step in pipeline_steps:
            if step["type"] == "transformer":
                transformer_id = step["id"]
                transformer_manager = step["manager"]
                input_ids = step.get("inputs", [])

                inputs = [
                    input_data[input_id]
                    for input_id in input_ids
                    if input_id in input_data
                ]

                if not inputs:
                    inputs = [
                        transformer_outputs[input_id]
                        for input_id in input_ids
                        if input_id in transformer_outputs
                    ]

                # We execute the transformer when we have all data
                if len(inputs) == len(input_ids):
                    transformed_data = transformer_manager.transform(*inputs)
                    transformer_outputs[transformer_id] = transformed_data

        self.elapsed_transform = self.benchmark.end("transform")
        self.logger.info("Finished transformers process.")

        return transformer_outputs

    def _process_output(self, pipeline_steps, transformer_outputs):
        self.logger.info("Starting output process (3/3).")
        self.benchmark.start("output")

        for step in pipeline_steps:
            if step["type"] == "output":
                output_id = step["id"]
                output_manager = step["manager"]
                input_ids = step.get("inputs", [])

                inputs = [
                    transformer_outputs[input_id]
                    for input_id in input_ids
                    if input_id in transformer_outputs
                ]

                # Executing the output method
                output_data = output_manager.put(*inputs)
                transformer_outputs[output_id] = output_data

        self.elapsed_output = self.benchmark.end("output")
        self.logger.info("Finished output process.")

    def get_summary(self):
        return {
            "elapsed_total": self.elapsed_total,
            "elapsed_input": self.elapsed_input,
            "elapsed_transform": self.elapsed_transform,
            "elapsed_output": self.elapsed_output,
        }
