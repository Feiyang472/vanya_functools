import sys
import time
from dataclasses import dataclass
from functools import cached_property
from multiprocessing.pool import ThreadPool


@dataclass
class Foo:
    @cached_property
    def bar(self):
        time.sleep(0.1)
        return "baz"


def test_stdlib_cached_property():
    with ThreadPool(4) as tpool:
        start = time.time()
        tpool.map(lambda foo: foo.bar, [Foo(), Foo()] * 2)
        duration = time.time() - start

        if sys.version_info < (3, 12):
            assert (round(duration, 1)) == 0.1
