Some very popular (and excellent) database query engines advertise the following python API
```python
import xxxdb
import pandas as pd

pandas_df = pd.DataFrame({"a": [42]})
xxxdb.sql("SELECT * FROM pandas_df")
```

To put it mildly, I imagine contributors are great pals with those at flake8, ruff, pyright, or mypy.

One might see the string-as-argument as a shorthand of the expressions API.

One might even be reminded that argument names can be omitted at struct init in Rust, if the argument names match those of fields.

The `evenshorterhand` module brings this idea to the extreme, where decorated functions will automatically absorb all relevant arguments needed for any callable which are not explictly provided.

```python
>>> from vanya_functools.evenshorterhand import Handless


>>> @Handless
... def add(a: int, b: int, /, *, c) -> int:
...     return a + b + c
... 
... 
... c = 3
... 
... add(1, 2)
6
```
Or you can do the following.
```python
from typing import NamedTuple
@dataclass
class Foo:
    bar: int
    baz: int

    @staticmethod
    def factory(bar: int):
        baz = bar * 3
        # as you can see, this is no longer a short hand
        # there is no hand
        return Handless(Foo)()

Foo.factory(1)
>>> Foo(bar=1, baz=3)
```

Your user is not in control of what arguments are passed to your APIs. You are.
Seize control now, do not let the big projects monopolize power.

