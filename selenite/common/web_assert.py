from typing import Optional

from loguru import logger
from selene import browser
from selene.core.exceptions import TimeoutException

from selenite.common import predicate

DEFAULT_MSG_TRUE = 'Condition should be true'
DEFAULT_MSG_FALSE = 'Condition should be false'
DEFAULT_MSG_EQUAL = 'Actual value {actual} is not equal to expected value {expected}'
DEFAULT_MSG_NOT_EQUAL = 'Actual value {actual} should not be equal to expected value {expected}'
DEFAULT_MSG_IS_NONE = 'Object should be None'
DEFAULT_MSG_IS_NOT_NONE = 'Object should not be None'
DEFAULT_MSG_IN = 'Object {obj} should be in container {container}'
DEFAULT_MSG_NOT_IN = 'Object {obj} should not be in container {container}'


class WebPredicate:

    @staticmethod
    def is_true(condition: bool, msg: Optional[str] = None) -> None:
        """
        Asserts that condition is True
        """
        return failure_with_hook(predicate.is_truthy(condition), msg or DEFAULT_MSG_TRUE)

    @staticmethod
    def is_false(condition: bool, msg: Optional[str] = None) -> None:
        """
        Asserts that condition is False
        """
        return failure_with_hook(predicate.is_truthy(not condition), msg or DEFAULT_MSG_FALSE)

    @staticmethod
    def is_equal(actual: object, expected: object, msg: Optional[str] = None) -> None:
        """
        Asserts that actual value is equal to expected value
        """
        msg = msg or DEFAULT_MSG_EQUAL.format(actual=actual, expected=expected)
        return failure_with_hook(predicate.equals(expected)(actual), msg)

    @staticmethod
    def is_in(obj: object, container: object, msg: Optional[str] = None) -> None:
        """
        Asserts that object is in container
        """
        msg = msg or DEFAULT_MSG_IN.format(obj=obj, container=container)
        return failure_with_hook(predicate.includes(obj)(container), msg)


browser_without_timeout = browser.with_(timeout=0)


def failure_with_hook(condition: bool, msg: Optional[str] = None) -> None:
    """
    Raises AssertionError if condition is False
    """
    failure = TimeoutException(f'\nReason: {msg}')

    if not condition:
        logger.error(msg)
        raise browser_without_timeout.wait.hook_failure(failure)


web_assert = WebPredicate()
