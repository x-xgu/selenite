import csv
import json
from typing import Any, List

import yaml


def load_json(file_path: str) -> Any:
    """
    Load json file from project

    Args:
        file_path (str): The path of the json file to be loaded.

    Returns:
        Any: The loaded json data.

    Example:
        >>> load_json('data.json')
        {'name': 'John', 'age': 30, 'city': 'New York'}
    """
    with open(file_path) as f:
        json_data = json.load(f)
    return json_data


def load_yml(file_path: str) -> Any:
    """
    Load yml file from project

    Args:
        file_path (str): The path of the yml file to be loaded.

    Returns:
        Any: The loaded yml data.

    Example:
        >>> load_yml('data.yml')
        {'name': 'John', 'age': 30, 'city': 'New York'}
    """
    with open(file_path) as f:
        yml_data = yaml.safe_load(f)
    return yml_data


def load_csv(file_path: str) -> List[List[str]]:
    """
    Load csv file from project and return list of lists

    Args:
        file_path (str): The path of the csv file to be loaded.

    Returns:
        List[List[str]]: The loaded csv data as a list of lists.

    Example:
        >>> load_csv('data.csv')
        [['name', 'age', 'city'], ['John', '30', 'New York'], ['Jane', '25', 'Los Angeles']]
    """
    data = []
    with open(file_path, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            data.append(row)
    return data
