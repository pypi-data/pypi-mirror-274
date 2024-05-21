# Cybertron: Transformation framework
Cybertron is a framework intended for retrieving data from one or several repositories, transforming it, and storing in output repositories.
For this purpose, pipelines are defined to manage the different stages of the process.

[![GoodCod3 - cybertron-framework](https://img.shields.io/static/v1?label=GoodCod3&message=cybertron-framework&color=blue&logo=github)](https://github.com/GoodCod3/cybertron-framework "Go to GitHub repo")
[![GitHub tag](https://img.shields.io/github/tag/GoodCod3/cybertron-framework?include_prereleases=&sort=semver&color=blue)](https://github.com/GoodCod3/cybertron-framework/releases/)
[![License](https://img.shields.io/badge/License-GNU_General_Public-blue)](#license)

## Authors
* Eduardo Martos Gómez <<emartos@natiboo.es>>
* Jonathan Rodríguez Alejos <<jonathan.rodriguez@goodcodesolution.com>>

## Pipeline
A pipeline refers to a series of steps (`Input`, `Transform`, `Mapper` and `Output`). Each process can have 1 or many pipelines and the orchestrator will decide how they will be executed.

## Orchestrator
It is responsible for executing the different steps of each pipeline. The core defines different types of orchestrator that can be imported from our code to specify how the steps of each process or set of pipelines will be executed.

### We have different types of orchestrators
#### Synchronous
The same process can have 1 or more pipeline defined, when it is executed it will do so sequentially, executing the same step for each pipeline. That is, first it will execute the Input of all the pipelines, then the transform together with the mapper of each pipeline and finally the output of each pipeline.

#### Sequence
This orchestrator allows us to better define the sequence of a pipeline. We can execute a `Transformer` with the data returned by another transformer or even indicate several of them.
If a transformer depends on more than 1 `Transformer` or `Input` step, then in the "transform" method we will receive a tuple with each set of data.
It also allows us to execute all Inputs in parallel to optimize the pipeline execution speed.

The way to define the pipeline for this orchestrator is as follows:

```python
from cybertron_framework.orchestrator.types.sequence import SequenceOrchestrator

pipeline_steps = [
    {"id": "input1", "type": "input", "manager": InputBigqueryManager()},
    {"id": "input2", "type": "input", "manager": InputPostgresManager()},
    {"id": "transformer1", "type": "transformer", "manager": TransformerBigqueryManager(), "inputs": ["input1"]},
    {"id": "transformer2", "type": "transformer", "manager": TransformerPostgresManager(), "inputs": ["input2"]},
    {"id": "transformer3", "type": "transformer", "manager": FinalTransformerManager(), "inputs": ["transformer1", "transformer2"]},
    {"id": "output1", "type": "output", "manager": FirstOutputManager(), "inputs": ["transformer3"]},
]

orchestrator = SequenceOrchestrator()
orchestrator.run(pipeline_steps)
```

---


## Pipeline stages

There are three different stages in the process:

1.  **Input.** The data is queried from the input repository and stored in memory.

Alternatively, the input data can be queried and processed record by record,

but it requires modifying the default orchestrator (see the _Orchestrator_ section below).


2.  **Transformation.** The information is transformed to send it to the output


3.  **Output.** The information is received transformed ready to be processed or saved in some external source (Bigquey, DB, Pub/Sub, etc...)


The workflow is modelled in the _Orchestrator_ class, that we will see in detail later.

---

# Class model
Before we start, please take into account that this framework relies heavily on the interfaces defined in the core.

When creating new functionalities, you should implement these interfaces to make sure that the pieces are correctly aligned and the classes exposes the expected methods.

Each endpoint of the flask application would have its own process or set of pipelines that will be executed by the selected orchestrator and must implement each layer of the pipeline that will be explained below.


## Project structure
Each Flask project will have two main directories (`app` & `core`)

### app
It is where we will have each of the endpoints of our application and where we can define generic steps for our pipelines.
Each endpoint will have its own directory where the different classes that belong to each step of the pipeline will be defined.

-  **app:** It is where we will have each of the endpoints of our application and where we can define generic steps for our pipelines.
	-  **endpoint1/**
		-  **input/**
		-  **transformer/**
		-  **output/**
		-  **orchestrator/ (Optional folder)**
		-  **include/**
		-  **main.py**
		-  **constants.py**
	-  **endpoint2/**
		- ...



#### input folder (First step of the pipeline)
In this directory we will have a class that will be responsible for downloading data from an external source (Database, Google Sheet, API, etc...). Our class must inherit from `from cybertron_framework.input.input_manager_interface import IInputManager` which has the following attributes:


* **get_id** : To identify each step and know which pipeline it belongs to, we must assign a unique string that allows us to identify our step within the execution process. This same ID must be used in other steps such as the Transformer and the Output. The value of this ID should be defined in the `constants.py` file inside the app.


* **get_data**: This is the method that the orchestrator will execute to start downloading the data, it must return a list of data.

	```python
	from cybertron_framework.input.input_manager_interface import IInputManager
	from src.app.resources.first_entry.constants import PROCESS_NAME


	class MyInputManager(IInputManager):
		def get_id(self):
			return PROCESS_NAME

		def get_data(self):
			# Here the request will be made to the external source (API, db, etc.) to obtain the data.
			return []
	```
---

#### transformer folder (Second step of the pipeline)
Sometimes we must transform the data we have downloaded (Parse data types, calculations, convert values, etc...) to prepare it for output. Here we define a class for the second step of the pipeline. The class must implement the methods of the `from cybertron_framework.transformer.transformer_manager_interface import ITransformerManager)` interface:

* **get_id**: Like the previous case, we must return a string with the pipeline ID, it must match the same one we used in the Input.

* **transform**: This is where we will have the logic to transform each data. In the `data` parameter of the method we will have all the information that the Input downloaded and we can modify it or return it as is.

	```python
	from cybertron_framework.transformer.transformer_manager_interface import (
		ITransformerManager,
	)
	from src.app.resources.first_entry.constants import PROCESS_NAME


	class FirstTransformerManager(ITransformerManager):
		def __init__(self, exclusions={}):
			self.exclusions = exclusions

		def get_id(self):
			return PROCESS_NAME

		def transform(self, data):
			"""
			Transforms the data
			"""
			transformed_data = transform_my_data(data)

			return transformed_data
	```
---

#### output folder (Last step of the pipeline)
This is the last step of the pipeline. This class is responsible for obtaining the transformed data and doing something with it, normally exporting it to another external source or executing some process.


* **get_id**: Like the previous case, we must return a string with the pipeline ID, it must match the same one we used in the Input and Transformer.

* **put**: This method receives a list of dictionaries with the transformed information.

```python
from typing import List

from cybertron_framework.environment.environment import Environment
from cybertron_framework.output.output_manager_interface import IOutputManager
from src.app.resources.first_entry.constants import PROCESS_NAME


class FirstOutputManager(IOutputManager):
    def __init__(self):
        environment = Environment()
        self.project = environment.get_value("BIGQUERY_PROJECT")
        self.dataset = environment.get_value("BIGQUERY_DATASET")
        self.table_name = environment.get_value("BIGQUERY_TABLE_TO_EXPORT")
        super().__init__()

    def get_id(self):
        return PROCESS_NAME

    def put(self, data: List[dict]):
		# Here we will process all the transformed information (Export to db, Bigquery, Pub/Sub, etc...)
        pass

```

**NOTE** ```We call the set of **Input + Transformer + Output**  "Pipeline", and normally are executed in that order.```

---

#### orchestrator folder (Optional folder)
**This directory is optional**, not all endpoints will have this directory. We will only create it when we want to modify the orchestrator and thus specify a new pipeline flow.

This class must implement the `from cybertron_framework.orchestrator.abstract_orchestrator import AbstractOrchestrator` interface and implement the following methods:

* **set_input_manager**: This method allows us to specify the transforms that we are going to register in the pipeline.

* **set_transformer_manager**: This method allows us to specify the data transformer class that we are going to register in the pipeline.

* **set_output_manager**: This method allows us to specify the output class of the pipeline.

* **run**: This method must have the logic of how the pipeline will be executed, what is the order of the steps, and where we must execute the corresponding methods of each step, etc...

* **get_summary**: We use this method to have a result after the "run" method finishes executing. Execution times can be recorded to know how long it takes to execute each step of the pipeline and a total computing time to return in this method or a simple success to know that the process has finished.

```python
from cybertron_framework.orchestrator.abstract_orchestrator import AbstractOrchestrator


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
		Here we will have the logic to execute the first step of the pipeline to download data.
        """
		return input_data

    def _process_data_transformation(self, input_data: dict):
        """
        Here we will have to execute the transformer corresponding to the information generated in the previous step. (We must compare the value of the "get_id" method of each step to know which one it corresponds to.
        """
        return transformed_data

    def _process_export_data(self, transformed_data: dict):
		"""
        Here we receive all the transformed data from all the pipelines and we can execute the output corresponding to each pipeline (Export to Bigquery, Postgres, Pub/Sub, etc...).
        """
		pass

    def get_summary(self):
        return {
            "elapsed_total": self.elapsed_total,
            "elapsed_input": self.elapsed_input,
            "elapsed_transform": self.elapsed_transform,
            "elapsed_output": self.elapsed_output,
        }

```
---

#### include folder (Generic services to use in each steps)
It contains all the generic connectors for our application (i.e. BigQuery client, SuccessFactors client, SAP client, etc.).
They can be simple functions or classes that centralize the business logic.

#### main.py (Running the flask endpoint)
Here we will find a class that inherits from the base class of the project (`from src.app.resources.base_view import BaseView`)
which offers us two main attributes:

* **environment** : Instance of the "Environment" class of the core, where we can obtain values of environment variables and validate whether they exist or not.

	```python
	from cybertron_framework.environment.environment import Environment
	```

* **orchestrator** : Instance of class `from cybertron_framework.orchestrator.types.synchronous import Orchestrator`
where we can record each step of our pipeline and execute the "run" method to execute the pipelines.

	```python
	from src.app.resources.base_view import BaseView
	from src.app.resources.first_entry.input.first_input_manager import (
		FirstInputManager,
		SecondInputManager,
	)
	from src.app.resources.first_entry.output.first_output_manager import (
		FirstOutputManager,
		SecondOutputManager,
	)
	from src.app.resources.first_entry.transformer.first_transformer_manager import (  # noqa: E501
		FirstTransformerManager,
		SecondTransformerManager,
	)


	class MainRoute(BaseView):
		def get(self):
			"""
			This is an example endpoint where we register 2 pipelines in the same process. When executing the "run" method of the orchestrator, the pipelines will be processed.
			---
			responses:
			200:
				description: Ok
				schema:
				type: string
			"""
			response_status = 200

			try:
				self.logger.info("Process started.")

				# Register Inputs
				self.orchestrator.set_input_manager(FirstInputManager())
				self.orchestrator.set_input_manager(SecondInputManager())

				# Register Transformers
				self.orchestrator.set_transformer_manager(
					FirstTransformerManager()
				)
				self.orchestrator.set_transformer_manager(
					SecondTransformerManager()
				)

				# Register Outputs
				self.orchestrator.set_output_manager(FirstOutputManager())
				self.orchestrator.set_output_manager(SecondOutputManager())

				self.orchestrator.run()
			except Exception as err:
				self.logger.error(str(err), from_exception=True)

				response_status = 500
				response_content = {"response": "KO", "error_message": str(err)}
			else:
				response_content = {
					"response": self.orchestrator.get_summary(),
				}

			return response_content, response_status

	```

## Global or generic steps for pipelines
In some cases we need to have different pipelines, either from the same process or different ones that share some steps and we want to reuse the same class in each pipeline. In that case we can replicate the directory structure `(Input, Transformer, Output, Include, Orchestrator, etc...)` at a level higher than the endpoint, so that it is global to all endpoints and each one imports it from there.

In this way we would have a project structure similar to the following:

-  **app/**
	-  **input/**
	-  **transformer/**
	-  **output/**
	-  **orchestrator/ (Optional folder)**
	-  **include/**
	-  **resources/**
		-  **endpoint1/**
			-  **input/**
			-  **transformer/**
			-  **output/**
			-  **orchestrator/ (Optional folder)**
			-  **include/**
			-  **main.py**
			-  **constants.py**
		-  **endpoint2/**
			- ...
-  **core/**
	- ...

## Entry points
There are one entry point that you can rewrite to adapt to your requirements:

1.  `web.py`: A Flask application that runs the application after the execution of an endpoint.


# How to develop
## Execute project in local
1. Create a python environment for the project with the command:

	`$ mkvirtualenv [PROJECT_NAME]`

	or if you have the python enviroment, you can just activate it:

	`$ workon [ENVIRONMENT_NAME]`

2. Install dependencies with the command

	`$ pip install -r code/requirements.txt`

3. Now you can run the Flask project with the command:

	`$ make run`

### Open the localhost
`http://127.0.0.1:5000/version`

### Open Swagger UI
`http://127.0.0.1:5000/swagger/`


# How to contribute
After clone repository


## 1.- Run test
```bash
make test
```

## 2.- Run lint and Isort
```bash
make lint && make isort
```

## 3.- Run pre commit command
This command will fix and run all lint rules (lint + Isort). You can configure this command with "pre-commit"
to run command on before make the Git commit automatically.
```bash
make pre-commit
```

# Managing dependencies in the project

## Add the new dependency with poetry
To add a new dependency in the project just run
```bash
$  poetry add Flask
```
or you can specify the dependency version with:
```bash
$  poetry add Flask===3.0.3
```
## Updating pip requirements.txt and update pip dependencies
After add the new poetry dependency we need to execute

```bash
$  make  freeze-dependencies
```
to update the requirements.txt

This will update the `requirements.txt` inside `code` folder.

Use the `make freeze-dependencies` command instead `pip freeze`.


And now we can execute

```bash
$  pip  install  -r  code/requirements.txt
```

to update local PIP dependencies.


## How to publish new version
Once we have done a merge of our Pull request and we have the updated master branch we can generate a new version. For them we have 3 commands that change the version of our library and generate the corresponding tag so that the Bitbucket pipeline starts and publishes our library automatically.

```bash
make release-patch
```

```bash
make release-minor
```

```bash
make release-major
```
