import functools

import allure
import pytest


def pending(test_fn):
    """
    Mark test as pending
    """
    def decorated(*args, **kwargs):
        test_fn(*args, **kwargs)
        pytest.skip('as pending')

    return decorated


@functools.wraps(pytest.mark.flaky)
def flaky(func=..., *, reruns: int = 0, reruns_delay: int = 0, condition=True):
    """
    Mark test as flaky
    """
    @functools.wraps(pytest.mark.flaky)
    def allurish_decorator(func_):
        return pytest.mark.flaky(
            reruns=reruns,
            reruns_delay=reruns_delay,
            condition=condition,
        )(allure.tag('flaky')(func_))

    return allurish_decorator(func) if callable(func) else allurish_decorator


class suite:

    @staticmethod
    @functools.wraps(pytest.mark.smoke)
    def smoke(func):
        """
        Mark test as smoke
        """
        return pytest.mark.smoke(allure.suite('smoke')(func))


class tag:

    @staticmethod
    @functools.wraps(pytest.mark.in_progress)
    def in_progress(func):
        """
        Mark test as in progress
        """
        return pytest.mark.in_progress(allure.tag('in_progress')(func))

    @staticmethod
    @functools.wraps(pytest.mark.release)
    def release(func):
        """
        Mark test as release
        """
        return pytest.mark.release(allure.tag('release')(func))
