from abc import ABC, abstractmethod


class Logger(ABC):
    """Abstraction du système de logging."""

    @abstractmethod
    def debug(self, message: str, **context) -> None:
        pass

    @abstractmethod
    def info(self, message: str, **context) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, **context) -> None:
        pass

    @abstractmethod
    def error(self, message: str, **context) -> None:
        pass