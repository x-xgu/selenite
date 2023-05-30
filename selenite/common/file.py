import json
from typing import Any

import yaml


def load_json(file_path: str) -> Any:
    """
    Load JSON file.
    """
    with open(file_path) as f:
        json_data = json.load(f)
    return json_data


def load_yml(file_path: str) -> Any:
    """
    Load YAML file.
    """
    with open(file_path) as f:
        yml_data = yaml.safe_load(f)
    return yml_data
