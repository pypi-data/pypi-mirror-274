import unittest

# from cybertron_framework.test_setup import *  # noqa: F401, F403
from unittest.mock import Mock, mock_open, patch

from cybertron_framework.environment.environment import Environment


class TestEnvironmentManager(unittest.TestCase):
    def setUp(self):
        self.environment = Environment()

    def test_set_environment_variables(self):
        environment_variables = {"VAR1": "value1", "VAR2": "value2"}
        self.environment.set_environment_variables(environment_variables)

        self.assertEqual(
            self.environment.environment_variables,
            environment_variables,
        )

    @patch("cybertron_framework.environment.environment.yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    def test_set_configuration_file(self, mock_open, mock_safe_load):
        configuration_file_path = "config.yaml"
        mock_safe_load.return_value = {"key": "value"}

        self.environment.set_configuration_file(configuration_file_path)

        mock_open.assert_called_once_with(configuration_file_path, "r")
        self.assertEqual(self.environment.config_variables, {"key": "value"})

    @patch("os.getenv")
    def test_check_raises_runtime_error_if_environment_variable_not_defined(
        self, mock_getenv
    ):
        mock_getenv.return_value = None
        self.environment.environment_variables = ["VAR1"]

        with self.assertRaises(RuntimeError) as context:
            self.environment.check()

        self.assertTrue(
            "Environment variable not defined: VAR1" in str(context.exception)
        )

    @patch("os.getenv", new=Mock())
    def test_get_value_returns_value_from_config_variables_if_key_exists(self):
        self.environment.config_variables = {"key": "value"}

        self.assertEqual(self.environment.get_value("key"), "value")

    @patch("os.getenv")
    def test_get_value_returns_value_from_environment_variables_if_key_exists(
        self, mock_getenv
    ):
        mock_getenv.return_value = "value"
        self.environment.environment_variables = ["key"]

        self.assertEqual(self.environment.get_value("key"), "value")

    def test_get_value_returns_none_if_key_does_not_exist_in_config_or_environment_variables(  # noqa: E501
        self,
    ):
        self.assertEqual(self.environment.get_value("nonexistent_key"), None)
