import unittest
from unittest.mock import patch

from freezegun import freeze_time

from cybertron_framework.helper.logger import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()

    @freeze_time("2022-1-1")
    @patch("cybertron_framework.helper.logger.logging")
    def test_info_logs_correctly(self, logging_mock):
        self.logger.info("Test message")

        logging_mock.info.assert_called_with("Test message")

    @patch("cybertron_framework.helper.logger.logging")
    @patch("traceback.format_exc")
    def test_warning_logs_correctly(self, mock_format_exc, logging_mock):
        mock_format_exc.return_value = "Traceback Error test"
        expected_result = "Test message | Traceback Error test"  # noqa: E501

        self.logger.warning("Test message", from_exception=True)

        logging_mock.warning.assert_called_with(expected_result)

    @patch("cybertron_framework.helper.logger.logging")
    @patch("traceback.format_exc")
    def test_error_logs_correctly(self, mock_format_exc, logging_mock):
        mock_format_exc.return_value = "Traceback Error test"
        expected_result = "Test message | Traceback Error test"  # noqa: E501

        self.logger.error("Test message", from_exception=True)

        logging_mock.error.assert_called_with(expected_result)

    @patch("cybertron_framework.helper.logger.logging")
    @patch("traceback.format_exc")
    def test_critical_logs_correctly(self, mock_format_exc, logging_mock):
        mock_format_exc.return_value = "Traceback Error test"
        expected_result = "Test message | Traceback Error test"  # noqa: E501

        self.logger.critical("Test message", from_exception=True)

        logging_mock.critical.assert_called_with(expected_result)
