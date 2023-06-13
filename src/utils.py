from pathlib import Path
from typing import Dict

import yaml


def add(a: int, b: int) -> int:
    return a + b


def load_config(path: Path) -> Dict:
    """Load config from yaml file.

    Args:
        path (Path): Path to YAML file.

    Returns:
        Dict: Dictionary containing configuration.
    """
    with open(path) as f:
        config = yaml.safe_load(f)
    if not isinstance(config, dict):
        return None
    return config
