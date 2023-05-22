import functools


def pipe(*functions):
    return functools.reduce(
        lambda f, g: lambda x: f(g(x)) if g else f(x),
        functions[::-1],
        lambda x: x) if functions else None
