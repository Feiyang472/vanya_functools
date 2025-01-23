import sys
import time
from dataclasses import dataclass
from functools import cached_property
from multiprocessing.pool import ThreadPool


@dataclass
class Foo:
    def __post_init__(self):
        self.__increment = 0

    @cached_property
    def bar(self):
        self.__increment += 1
        time.sleep(0.1)
        return self.__increment


def test_stdlib_cached_property():
    with ThreadPool(4) as tpool:
        start = time.time()
        result = tpool.map(lambda foo: foo.bar, [Foo(), Foo()] * 2)
        duration = time.time() - start

        if sys.version_info < (3, 12):
            assert (round(duration, 1)) == 0.1
            assert result == [1, 1, 1, 1]
        else:
            assert result == [2, 2, 2, 2]
