from dataclasses import dataclass
from multiprocessing.pool import ThreadPool
from typing_extensions import Self
from vanya_functools.lazylock import Kundera


@dataclass(slots=True, frozen=True)
class Node:
    value: list[Self] | None = None

    @Kundera
    def size(self):
        if self.value is None:
            return 1

        with ThreadPool() as pool:
            return 1 + sum(pool.map(lambda foo: foo.size, self.value))


def test_no_deadlock():
    assert Node([Node(), Node()]).size == 3
