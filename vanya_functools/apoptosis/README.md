> Apoptosis is a form of programmed cell death.

`vanya_functools.apoptosis` is the module for sudden programmed death of python variables.

The `Ruthless` decorator makes any value returned by the decorated callable *expire* after a specified time.
```python
>>> import copy
>>> import time
>>> from vanya_functools.apoptosis import Ruthless
>>> from dataclasses import dataclass

>>> @dataclass
... class Foo:
...    arg: int

>>> @Ruthless  # default 1.0 second time-to-live
... def bar(arg):
...     return Foo(arg)

>>> foo1 = bar(1)
>>> time.sleep(0.3)
>>> foo2 = bar(2)
>>> dolly = copy.copy(foo1)
>>> print(foo1, foo2, dolly)  # the good old times when all things were access
Foo(arg=1) Foo(arg=2) Foo(arg=1)

>>> time.sleep(0.71)
>>> try:
...     print(foo1, foo2, dolly)
... except ReferenceError as err:
...     print("foo1 is no longer accessible because {} but foo2 is still {}".format(err, foo2))
...     print("dolly={} is available because you have transferred ownership to your current scope by shallow copying it.".format(dolly))
foo1 is no longer accessible because weakly-referenced object no longer exists but foo2 is still Foo(arg=2)
dolly=Foo(arg=1) is available because you have transferred ownership to your current scope by shallow copying it.
>>> time.sleep(0.4)
>>> try:
...     print(foo2)
... except ReferenceError as err:
...     print("Now only dolly={} remains...".format(dolly))
Now only dolly=Foo(arg=1) remains...

```

`Ruthless` isn't your run-of-the-mill TTL cache.
It forces the user to make a choice:
1. *Explicit Consumption*: copy your data or grab the specific attributes you need.
2. *Go fast or go home*: Write efficient algorithms which finish execution before reference expires.