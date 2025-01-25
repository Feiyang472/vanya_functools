# vanya_functools
![](https://github.com/Feiyang472/vanya_functools/actions/workflows/pylint.yml/badge.svg)
![](https://github.com/Feiyang472/vanya_functools/actions/workflows/ruff.yml/badge.svg)
![](https://github.com/Feiyang472/vanya_functools/actions/workflows/pytest.yml/badge.svg)


Vanya is the nickname of [Ivan Fyodorovich Karamazov](https://en.wikipedia.org/wiki/Ivan_Fyodorovich_Karamazov).

`vanya_functools` provides functional programming tools in python which can be achieved, but not necessarily should be achieved.

## Installation

To install `vanya_functools`, use pip:

```sh
pip install vanya_functools
```

# Usage
- `lazylock`: cached property descriptor which behaves differently to the builtin `functools.cached_property` in multithreaded environment.
- `evenshorterhand`: the world is there for the taking
- `apoptosis`: work in progress

Consult module level docs for detailed descriptions.

## Testing

`vanya_functools` uses pytest + doctest to test all snippets in READMEs and in code.
