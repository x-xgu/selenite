from typing import Callable, Optional


class Settings:

    def __init__(
            self,
            source: Callable[[str, Optional[str]], Optional[str]] = lambda _: None,
            *more: Callable[[str, Optional[str]], Optional[str]]
    ):
        sources = [source, *more]
        from functools import reduce
        self._source = reduce(
            (lambda f, g: lambda key, default:
            f(key, g(key, default)) if g else f(key, None)),
            sources[::-1],
            lambda _, default: default
        )

    @property
    def source(self):
        return self._source


def default(value):
    def decorator(method):
        import functools

        @functools.wraps(method)
        def fun(self: Settings):
            maybe_sourced = self.source(method.__name__, None)

            sourced_or_value = \
                maybe_sourced if maybe_sourced is not None \
                    else value

            original_type = type(value)

            return original_type(sourced_or_value)

        return property(fun)

    return decorator
