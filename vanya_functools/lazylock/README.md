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


This module provides a near-replacement for `cached_property` which uses a per-object thread lock.
*Cache Is Elsewhere*, and it works on `__slots__`.
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
