import unittest
from unittest.mock import patch

from cybertron_framework.helper.benchmark import Benchmark


class TestBenchmark(unittest.TestCase):
    def setUp(self):
        self.benchmark = Benchmark()

    @patch("time.time", side_effect=[0, 5])
    def test_end_returns_correct_duration(self, mock_time):
        self.benchmark.start("test_key")

        duration = self.benchmark.end("test_key")

        self.assertEqual(duration, "5")

    @patch("time.time", side_effect=[0, 5, 10])
    def test_end_returns_correct_duration_after_multiple_starts(
        self, mock_time
    ):
        self.benchmark.start("test_key1")
        self.benchmark.start("test_key2")

        duration = self.benchmark.end("test_key2")

        self.assertEqual(duration, "5")

    @patch("time.time", side_effect=[0, 5])
    def test_end_raises_key_error_if_key_not_present(self, mock_time):
        with self.assertRaises(KeyError):
            self.benchmark.end("nonexistent_key")
