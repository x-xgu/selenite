from typing import List, Dict, Any

import cv2
import numpy as np


def zip_dict(keys: List[str], *values: List) -> List[Dict[str, str]]:
    return [dict(zip(keys, value)) for value in values]


def format_decimal_number_with_commas(number: float) -> str:
    formatted_number = f'{float(number):,}'
    return formatted_number


def bytes_to_numpy(bytes_data: bytes) -> np.ndarray:
    nparr = np.frombuffer(bytes_data, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)


def convert_sec_to_ms(timeout: float) -> float:
    return timeout * 1000


def copy_object_without_attrs(obj: Any, *attrs: str) -> Any:
    return type(obj)(
        **{
            k: v
            if k not in attrs
            else
            None
            for k, v
            in vars(obj).items()
        }
    )
