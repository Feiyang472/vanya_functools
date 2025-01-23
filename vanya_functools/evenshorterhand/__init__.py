# pylint: disable=R0903
"""
This module provides the `Handless` decorator which allows functions to automatically
use variables from the calling scope if they are not provided as arguments.
"""

import inspect
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

class Handless:
    """
    A decorator that allows functions to automatically use variables from the calling scope
    if they are not provided as arguments.

    Example:
        >>> @Handless
        ... def add(a, b):
        ...     return a + b
        ...
        >>> a = 1
        >>> b = 2
        >>> add()
        3
    """

    def __init__(self, callable_: Callable[P, R]) -> None:
        """
        Initialize the Handless decorator with a callable.

        Args:
            callable_ (Callable[[P], R]): The callable to be decorated.
        """
        self.callable_ = callable_
        self.signature = inspect.signature(self.callable_)
        self.__signature__ = self.signature

    def __call__(self, *args, **kwargs) -> R:
        """
        Call the decorated function, using variables from the calling scope if necessary.

        Args:
            *args: Positional arguments for the callable.
            **kwargs: Keyword arguments for the callable.

        Returns:
            The result of the callable.

        Example:
            >>> @Handless
            ... def multiply(x, y):
            ...     return x * y
            ...
            >>> x = 3
            >>> y = 4
            >>> multiply()
            12
        """
        stack_above = inspect.currentframe().f_back.f_locals
        provided = self.signature.bind_partial(*args, **kwargs).arguments
        for param in self.signature.parameters.values():
            if (
                (param.name not in provided)
                and (param.kind is not param.POSITIONAL_ONLY)
                and param.name in stack_above
            ):
                kwargs[param.name] = stack_above[param.name]

        return self.callable_(*args, **kwargs)
