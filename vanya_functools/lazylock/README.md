# Lazylock

# Introduction

CPython is not always intuitive.

Consider the following snippet, how long do you expect it to take, and what do you expect it to print?
```python
from functools import cached_property
from multiprocessing.pool import ThreadPool
import time


class Foo:
    def __init__(self):
        self.__increment = 0

    @cached_property
    def bar(self):
        # obviously, mutating here is quite a crazy thing to do.
        # in real life you might be reading a changing database
        self.__increment += 1
        time.sleep(0.1)
        return self.__increment

with ThreadPool(4) as tpool:
    print(tpool.map(lambda foo: foo.bar, [Foo(), Foo()] * 2))
```

Prior to python 3.12, this takes 0.2 seconds and returns `[1, 1, 1, 1]` because there is one thread lock per descriptor, which means all instances will share the same lock for the same property.

After python 3.12, this takes 0.1 seconds and returns `[2, 2, 2, 2]` because there is *no* lock at all!

This module provides a near-replacement for `cached_property`: `Kundera`, which uses a per-object-per-property thread lock.

*Cache Is Elsewhere*, so it also works on objects with `__slots__`.

```python
from dataclasses import dataclass
from functools import cached_property
from multiprocessing.pool import ThreadPool
import time

from vanya_functools.lazylock import Kundera


@dataclass(slots=True)
class Foo:
    @Kundera
    def bar(self):
        time.sleep(1)
        return 1

with ThreadPool(4) as tpool:
    print(tpool.map(lambda foo: foo.bar, [Foo(), Foo()] * 2))
```

## Deadlock
It is very easy to construct a scenario where using `functools.cached_property (<3.12)` causes deadlock but using `Kundera` does not.

```python
from functools import cached_property
from multiprocessing.pool import ThreadPool
from typing_extensions import Self


class Node:
    def __init__(self, value: list[Self] | None = None):
        self.value = value

    @cached_property
    def size(self):
        if self.value is None:
            return 1

        with ThreadPool() as tpool:
            return 1 + sum(tpool.map(lambda foo: foo.size, self.value))

Node(
    [Node()]
).size  # Deadlock!


@dataclass(slots=True)
class Node:
    value: list[Self] | None = None

    @Kundera
    def size(self):
        if self.value is None:
            return 1

        with ThreadPool() as pool:
            return 1 + sum(pool.map(lambda foo: foo.size, self.value))

Node(
    [Node()]
).size  # all is well
```

## Why dataclass
In essence, `Kundera` needs to modify the instantiation process of a class. This could be achieved by modifying `__init__`/`__new__`, or forcing the user to adopt a superclass/metaclass. All of these options imply constraints
on how the user defines their class. In comparison, abusing `dataclass` is probably the lesser evil.
