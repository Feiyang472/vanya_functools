CPython is not always intuitive.

Consider the following snippet, how long do you expect it to take?
```python
from functools import cached_property
from multiprocessing.pool import ThreadPool
import time


class Foo:
    @cached_property
    def bar(self):
        time.sleep(1)
        return 1

with ThreadPool(4) as tpool:
    print(tpool.map(lambda foo: foo.bar, [Foo(), Foo()] * 2))
```
The answer is 2.0 seconds because there is only one Lock.

This module provides a near-replacement for `cached_property` which uses a per-object lock.
*Cache Is Elsewhere*, and it works on `__slots__`.
```python
from dataclasses import dataclass
from functools import cached_property
from multiprocessing.pool import ThreadPool
import time

from vanya_functools.vanya_functools.lazylock import Kundera


@dataclass(slots=True)
class Foo:
    @Kundera
    def bar(self):
        time.sleep(1)
        return 1

with ThreadPool(4) as tpool:
    print(tpool.map(lambda foo: foo.bar, [Foo(), Foo()] * 2))
```
