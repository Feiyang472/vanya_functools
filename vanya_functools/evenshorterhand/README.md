Some very popular (and excellent) database query engines and numerical expression evaluators advertise the following python API
```python
import xxxdb
import pandas as pd

pandas_df = pd.DataFrame({"a": [42]})
xxxdb.sql("SELECT * FROM pandas_df")
a = np.arange(1e5)
xxxdb.evaluate("a + 1")
```

To put it mildly, I am not sure I can put it mildly.

The `evenshorterhand` module brings this idea to the extreme, where decorated callable will automatically absorb all relevant arguments which are needed but not explictly provided.

```python
>>> from vanya_functools.evenshorterhand import Handless


>>> @Handless
... def add(a: int, b: int, /, *, c) -> int:
...     return a + b + c

>>> c = 3
>>> add(1, 2)
6

```

You can apply it to class instantiators.
```python
>>> from dataclasses import dataclass
>>> from typing import NamedTuple
>>> @dataclass
... class Foo:
...     bar: int
...     baz: int
...     @staticmethod
...     def factory(bar: int):
...         baz = bar * 3
...         # as you can see, this is no longer a short hand
...         # there is no hand
...         return Handless(Foo)()
...
>>> Foo.factory(1)
Foo(bar=1, baz=3)

```

Your user is not in control of what arguments are passed to your APIs. You are.

***Seize control, now,*** do not let the big projects monopolize power.

