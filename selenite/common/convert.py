from typing import List, Dict, Any

import cv2
import numpy as np


def zip_dict(
        keys: List[str],
        *values: List
) -> List[Dict[str, str]]:
    """
    Given a list of keys and a list of values, zip them together into a list of dictionaries.
    """
    return [
        dict(zip(keys, value))
        for value in values
    ]


def format_decimal_number_with_commas(
        number: float
) -> str:
    """
    Convert a decimal number to a string with commas.
    """
    formatted_number = f'{float(number):,}'
    return formatted_number


def bytes_to_numpy(
        bytes_data: bytes
) -> np.ndarray:
    """
    Convert bytes to numpy array.
    """
    nparr = np.frombuffer(bytes_data, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)


def convert_sec_to_ms(
        timeout: float
) -> float:
    """
    Convert seconds to milliseconds.
    """
    return timeout * 1000


def copy_object_without_attrs(
        obj: Any,
        *attrs: str,
        default: Any = None
) -> Any:
    """
    Copy an object without the specified attributes.
    """
    return type(obj)(
        **{
            k: v
            if k not in attrs
            else
            default
            for k, v
            in vars(obj).items()
        }
    )
