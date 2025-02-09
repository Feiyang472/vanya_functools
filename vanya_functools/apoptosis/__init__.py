# pylint: disable=R0903
"""
This module provides the Ruthless decorator which mark returned values of callables
with a lifetime, after which they will be inaccessible unless explicitly cloned or
consumed.
"""

import heapq
import threading
import time
from typing import Callable, Generic, ParamSpec, TypeVar
import weakref

KT = TypeVar("KT")
P = ParamSpec("P")
R = TypeVar("R")


class GarbageRobbist(Generic[R]):
    """Keep"""

    def __init__(self, default_ttl: float, collection_freq: float):
        self.__stop_event = threading.Event()
        self.default_ttl = default_ttl
        self.lock = threading.RLock()
        self.__deadlines: list[tuple[float, R]] = []
        self.__thread = threading.Thread(target=self.__garbage_robbery, daemon=True)
        self.__freq = collection_freq
        super().__init__()

    def __garbage_robbery(self):
        while not self.__stop_event.is_set():

            while self.__deadlines and self.__deadlines[0][0] < time.time():
                heapq.heappop(self.__deadlines)
            time.sleep(self.__freq)

    def __del__(self):
        if not self.__thread._started.is_set():
            return
        self.__stop_event.set()
        self.__thread.join()

    def push_value(self, value: R, ttl: float | None = None):
        """Push a value in the heap for auto-poping after some time."""
        ttl = ttl or self.default_ttl
        if not self.__thread.is_alive():
            self.__thread.start()
        heapq.heappush(self.__deadlines, (time.time() + ttl, value))


class Ruthless(Generic[P, R]):
    """
    A decorator which wraps a function to return a result which becomes corrupted after 1.0 seconds.

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
