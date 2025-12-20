import sys
from pathlib import Path
from loguru import logger

from churn_gym.infrastructure.utils.config_loader import load_yaml_config
from churn_gym.infrastructure.utils.root_finder import get_repository_root


def configure_logging(env: str = "dev") -> None:
    """
    Configure Loguru sinks (console + file).

    Cette fonction doit être appelée UNE SEULE FOIS
    au point d'entrée de l'application (API, script, CLI).
    """

    # ── Load config lazily (no side effects at import time)
    root = get_repository_root()
    config_path = root / "configs/paths.yaml"
    cfg = load_yaml_config(config_path)

    logger_dir = root / Path(cfg["paths"]["logger_dir"])
    logger_dir.mkdir(parents=True, exist_ok=True)

    # ── Reset default handlers
    logger.remove()

    # ── Console sink
    logger.add(
        sys.stdout,
        level="DEBUG" if env == "dev" else "INFO",
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{name}</cyan> | "
            "{message} | {extra}"
        ),
        enqueue=True,  # safe for async / multiprocessing
    )

    # ── File sink (JSON structured logs)
    logger.add(
        logger_dir / "churn_gym.log",
        rotation="10 MB",
        retention="10 days",
        level="INFO",
        serialize=True,
        enqueue=True,
    )