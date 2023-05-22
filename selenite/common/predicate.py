from typing import Any


def is_truthy(something: Any) -> bool:
    return bool(something) if not something == '' else True


def equals_ignoring_case(expected) -> callable:
    return lambda actual: str(expected).lower() == str(actual).lower()


def equals(expected, ignore_case=False) -> callable:
    return (
        lambda actual: expected == actual
        if not ignore_case
        else equals_ignoring_case(expected)
    )


def includes_ignoring_case(expected) -> callable:
    return lambda actual: str(expected).lower() in str(actual).lower()


def includes(expected, ignore_case=False) -> callable:
    def fn(actual):
        try:
            return (
                expected in actual
                if not ignore_case
                else includes_ignoring_case(expected)
            )
        except TypeError:
            return False

    return fn
