import random
import string
from typing import Union, Any


def random_int(
        min_value: int = 0,
        max_value: int = 1000
) -> int:
    """
    Generate a random integer between min_value and max_value
    """
    return random.randint(min_value, max_value)


def random_float(
        min_value: float = 0.0,
        max_value: float = 1.0,
        num_decimal_places: int = 2,
        to_str: bool = False
) -> Union[str, float]:
    """
    Generate a random float between min_value and max_value
    """
    def _random_float_to_str(num):
        return '{:.{dp}f}'.format(num, dp=num_decimal_places)

    value = round(random.uniform(min_value, max_value), num_decimal_places)
    if to_str:
        return _random_float_to_str(value)

    return value


def random_string(
        length: int = 10
) -> str:
    """
    Generate a random string of lowercase letters
    """
    letters = string.ascii_lowercase
    return ''.join(
        random.choice(letters)
        for _ in range(length)
    )


def random_bool() -> bool:
    """
    Generate a random boolean value
    """
    return bool(random.getrandbits(1))


def random_choice(
        lst: list
) -> Any:
    """
    Return a random element from a list
    """
    return random.choice(lst)


def random_chinese(
        length: int = 5
) -> str:
    """
    Generate a random string of Chinese characters
    """
    return ''.join(
        chr(random.randint(0x4e00, 0x9fa5))
        for _ in range(length)
    )
