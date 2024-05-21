import unittest
from unittest.mock import MagicMock

from cybertron_framework.transformer.transformer_manager_interface import (
    ITransformerManager,
)


class TestTransformerManager(unittest.TestCase):
    def setUp(self):
        self.manager = ITransformerManager()

    def test_fail_get_id(self):
        with self.assertRaises(NotImplementedError):
            self.manager.get_id()

    def test_fail_transform(self):
        data = {}
        with self.assertRaises(NotImplementedError):
            self.manager.transform(data)

    def test_success_transform(self):
        data = {}
        transformer_mock = MagicMock(spec=ITransformerManager)
        transformer_mock.get_id.return_value = "1"
        transformer_mock.transform.return_value = {"a": 1}

        result_id = transformer_mock.get_id(data)
        result_transform = transformer_mock.transform(data)

        self.assertEqual(result_id, "1")
        self.assertEqual(result_transform, {"a": 1})
