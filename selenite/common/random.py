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


def random_number_string(
        length: int,
        min_value: Union[int, float],
        max_value: Union[int, float],
        separator: str
) -> str:
    def get_decimal_places(value: float) -> int:
        if isinstance(value, float):
            return len(str(value).split(".")[1])
        return 0

    if isinstance(min_value, float) or isinstance(max_value, float):
        random_fn = random_float
        params = {
            'min_value': min_value,
            'max_value': max_value,
            'num_decimal_places': max(get_decimal_places(min_value), get_decimal_places(max_value)),
            'to_str': True
        }
    else:
        random_fn = random_int
        params = {
            'min_value': min_value,
            'max_value': max_value
        }
    return separator.join(
        [
            str(random_fn(**params))
            for _ in range(length)
        ]
    )
