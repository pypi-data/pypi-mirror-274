import logging
import traceback

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Logger:
    """
    Logs messages to the stdout
    """

    def info(self, message):
        return logging.info(message)

    def warning(self, message, from_exception=False):
        return logging.warning(
            self.__build_error_message(message, from_exception)
        )

    def error(self, message, from_exception=False):
        return logging.error(
            self.__build_error_message(message, from_exception)
        )

    def critical(self, message, from_exception=False):
        return logging.critical(
            self.__build_error_message(message, from_exception)
        )

    def __build_error_message(self, message, from_exception=False):
        if from_exception:
            message = f"{message} | {traceback.format_exc()}"

        return message
