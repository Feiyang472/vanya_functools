import inspect
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class Handless:
    def __init__(self, callable: Callable[[P], R]) -> None:
        self.callable = callable

        self.signature = inspect.signature(self.callable)
        self.__signature__ = self.signature

    def __call__(self, *args, **kwargs) -> R:
        stack_above = inspect.currentframe().f_back.f_locals
        provided = self.signature.bind_partial(*args, **kwargs).arguments
        for param in self.signature.parameters.values():
            if (
                (param.name not in provided)
                and (param.kind is not param.POSITIONAL_ONLY)
                and param.name in stack_above
            ):
                print(param.name)
                kwargs[param.name] = stack_above[param.name]

        return self.callable(*args, **kwargs)
