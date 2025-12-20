from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
import yaml
from .exceptions import ConfigLoadingError



def load_yaml_config(path: str | Path) -> Dict[str, Any]:
    """
    Charge un fichier YAML et retourne un dictionnaire Python.

    Args:
        path: chemin vers le YAML (ex: configs/training.yaml)

    Returns:
        dict: contenu du YAML

    Raises:
        ConfigError: si fichier introuvable ou YAML invalide
    """
    path = Path(path)
    if not path.exists():
        raise ConfigLoadingError(f"Config introuvable: {path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigLoadingError(f"YAML invalide ({path}): {e}") from e

    if data is None:
        raise ConfigLoadingError(f"Config vide: {path}")

    return data