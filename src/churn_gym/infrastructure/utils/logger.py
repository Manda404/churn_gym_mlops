from loguru import logger
import sys
from pathlib import Path


def configure_logging(env: str = "dev") -> None:
    logger.remove()

    logger.add(
        sys.stdout,
        level="DEBUG" if env == "dev" else "INFO",
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{name}</cyan> | "
            "{message} | {extra}"
        ),
    )

    logger.add(
        Path("logs/app.log"),
        rotation="10 MB",
        retention="10 days",
        level="INFO",
        serialize=True,  # JSON → prod / observabilité
    )
