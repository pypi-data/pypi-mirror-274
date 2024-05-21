import unittest
from unittest.mock import MagicMock

from cybertron_framework.environment.environment_interface import IEnvironment


class TestIEnvironment(unittest.TestCase):
    def setUp(self):
        self.manager = IEnvironment()

    def test_fail_set_environment_variables(self):
        with self.assertRaises(NotImplementedError):
            variables = []
            self.manager.set_environment_variables(variables)

    def test_fail_set_configuration_file(self):
        with self.assertRaises(NotImplementedError):
            file_path = ""
            self.manager.set_configuration_file(file_path)

    def test_fail_check(self):
        with self.assertRaises(NotImplementedError):
            self.manager.check()

    def test_fail_get_value(self):
        with self.assertRaises(NotImplementedError):
            key = ""
            self.manager.get_value(key)

    def test_success_methods(self):
        transformer_mock = MagicMock(spec=IEnvironment)
        transformer_mock.set_environment_variables.return_value = "1"
        transformer_mock.set_configuration_file.return_value = "2"
        transformer_mock.check.return_value = "3"
        transformer_mock.get_value.return_value = "4"

        result_set_environment_variables = (
            transformer_mock.set_environment_variables()
        )
        result_set_configuration_file = (
            transformer_mock.set_configuration_file()
        )
        result_check = transformer_mock.check()
        result_get_value = transformer_mock.get_value("a")

        self.assertEqual(result_set_environment_variables, "1")
        self.assertEqual(result_set_configuration_file, "2")
        self.assertEqual(result_check, "3")
        self.assertEqual(result_get_value, "4")
