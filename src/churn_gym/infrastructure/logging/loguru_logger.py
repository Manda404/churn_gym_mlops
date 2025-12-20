from loguru import logger
from churn_gym.domain.interfaces.logger import Logger


class LoguruLogger(Logger):
    def debug(self, message: str, **context) -> None:
        logger.bind(**context).debug(message)

    def info(self, message: str, **context) -> None:
        logger.bind(**context).info(message)

    def warning(self, message: str, **context) -> None:
        logger.bind(**context).warning(message)

    def error(self, message: str, **context) -> None:
        logger.bind(**context).error(message)
