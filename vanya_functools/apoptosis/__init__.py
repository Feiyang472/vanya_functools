# pylint: disable=R0903
"""
This module provides the Ruthless decorator which mark returned values of callables
with a lifetime, after which they will be inaccessible unless explicitly cloned or
consumed.
"""

import heapq
import math
from queue import Queue
import threading
import time
import weakref
from types import MethodType
from typing import Callable, Concatenate, Generic, ParamSpec, Type, TypeVar, overload

from typing_extensions import Self

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")


class GarbageRobbist(Generic[R]):
    """
    Maintain the only strong references to weakreffable objects in a queue.
    Periodically pop expired objects out.
    """

    def __init__(self, ttl: float, collection_freq: float):
        self.ttl = ttl
        self.__deadlines = Queue[tuple[float, R]]()
        self.__stop_event = threading.Event()
        self.__freq = collection_freq
        threading.Thread(
            target=self.__garbage_robbery, args=(weakref.ref(self),), daemon=True
        ).start()

    @classmethod
    def __garbage_robbery(cls, ref: Callable[[], Self]):

        while (self := ref()) is not None and not self.__stop_event.is_set():

            while not self.__deadlines.empty() and self.__deadlines.queue[0][0] < time.time():
                self.__deadlines.get()
            time.sleep(self.__freq)

            del self

    def __del__(self):
        self.__stop_event.set()

    def push_value(self, value: R):
        """Push a value in the queue for auto-poping after some time."""
        self.__deadlines.put((time.time() + self.ttl, value))


class Ruthless(Generic[P, R]):
    """
    A decorator which wraps a function to return a result which becomes corrupted after the specified ttl.

    Example:
    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class Foo:
    ...    arg: int
    >>> @Ruthless
    ... def bar(arg):
    ...     return Foo(arg)
    >>> import time
    >>> baz1 = bar(1)
    >>> time.sleep(0.3)
    >>> baz2 = bar(2)
    >>> print(baz1, baz2)
    Foo(arg=1) Foo(arg=2)
    >>> time.sleep(0.71)
    >>> try:
    ...     print(baz1, baz2)
    ... except ReferenceError as err:
    ...     print("baz1 is no longer accessible but baz2 is still {}".format(baz2))
    baz1 is no longer accessible but baz2 is still Foo(arg=2)
    """
    def __init__(self, callable_: Callable[P, R], ttl: float = 1.0, freq: float = 0.01):
        self.callable_ = callable_
        self.__cache = GarbageRobbist[R](ttl, freq)

    def __call__(self, *args: P.args, **kwds: P.kwargs) -> R:
        result = self.callable_(*args, **kwds)
        self.__cache.push_value(result)
        return weakref.proxy(result)
