from typing import Optional

from selenite.conf.allure import report


def _step(description: Optional[str] = None):
    def decorated(fn):
        if description:
            fn.__name__ = description.replace(' ', '_')
        return report.step(fn, display_context=False)()

    return decorated


def given(precondition: Optional[str] = None):
    return _step(precondition)


def when(act: Optional[str] = None):
    return _step(act)


def then(assertion: Optional[str] = None):
    return _step(assertion)
