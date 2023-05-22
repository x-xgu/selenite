from __future__ import annotations

from typing import List


class Option:

    @staticmethod
    def s_from(cls) -> List[Option]:
        return [
            Option.from_(field)
            for field in cls.__dict__.values()
            if Option.in_(field)
        ]

    @staticmethod
    def from_(prop) -> Option:
        return prop.fget.option

    @staticmethod
    def in_(field) -> bool:
        return hasattr(field, 'fget') and hasattr(field.fget, 'option')

    @staticmethod
    def register_all(from_cls, in_parser):
        for option in Option.s_from(from_cls):
            option.register(in_parser)

    @staticmethod
    def default(value, **attributes):
        def decorator(fun_on_self_with_request):
            option = Option(
                f'--{fun_on_self_with_request.__name__}',
                action='store',
                default=value,
                type=type(value),
                **attributes)

            def fun(self):
                return option.value(self.request)

            fun.option = option

            return property(fun)

        return decorator

    def __init__(self, name, **attributes):
        self.name = name
        self.attributes = attributes

    def value(self, from_request):
        return from_request.config.getoption(self.name)

    def register(self, parser):
        parser.addoption(self.name, **self.attributes)
