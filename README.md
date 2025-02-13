# vanya_functools
![](https://github.com/Feiyang472/vanya_functools/actions/workflows/pylint.yml/badge.svg)
![](https://github.com/Feiyang472/vanya_functools/actions/workflows/ruff.yml/badge.svg)
![](https://github.com/Feiyang472/vanya_functools/actions/workflows/pytest.yml/badge.svg)
![codecov](https://codecov.io/gh/Feiyang472/vanya_functools/graph/badge.svg?token=LDZ8IZHC8Y)


Vanya is the nickname of [Ivan Fyodorovich Karamazov](https://en.wikipedia.org/wiki/Ivan_Fyodorovich_Karamazov).

`vanya_functools` provides function decorators and descriptors in python which can be achieved, but not necessarily should be achieved.

## Installation

To install `vanya_functools`, use pip:

```sh
pip install vanya_functools
```

# Usage
- `lazylock`: cached property descriptor which behaves differently to the builtin `functools.cached_property` in multithreaded environment.
- `evenshorterhand`: the world is there for the taking.
- `apoptosis`: force downstream user of your function to write faster code by binding **lifetime** of data to functions.

Consult module level docs for detailed descriptions.

## Testing

`vanya_functools` uses pytest + doctest to test all snippets in all markdown files and in code.
