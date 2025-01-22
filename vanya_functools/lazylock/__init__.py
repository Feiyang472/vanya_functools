import functools
from dataclasses import MISSING, Field
from threading import Lock
from typing import (
    Callable,
    Generic,
    ParamSpec,
    Type,
    TypeVar,
    overload,
)

from typing_extensions import Self

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")


class LazyLock(Generic[P, R]):
    """
    A thread-safe lazy initialization lock for a callable.

    Ensures that the callable is only executed once and caches the result.
    """

    _NOT_FOUND = object()

    def __init__(self, callable: Callable[P, R]) -> None:
        """
        Initialize the LazyLock with a callable.

        Args:
            callable (Callable[P, R]): The callable to be lazily executed.
        """
        self.lock = Lock()
        self.callable = callable
        self.result = self.__class__._NOT_FOUND

    def __call__(self, *args: P.args, **kwargs: P.kwargs):
        """
        Execute the callable if it hasn't been executed yet, otherwise return the cached result.

        Args:
            *args: Positional arguments for the callable.
            **kwargs: Keyword arguments for the callable.

        Returns:
            The result of the callable.
        """
        val = self.result
        if val is self.__class__._NOT_FOUND:
            with self.lock:
                # check if another thread filled cache while we awaited lock
                val = self.result
                if val is self.__class__._NOT_FOUND:
                    val = self.callable(*args, **kwargs)
                    self.result = val
        return val


class Kundera(Generic[T, R]):
    """
    A descriptor that uses LazyLock to lazily initialize a method.

    Usage:
    ```python

    @dataclass
    class Foo:
        @Kundera
        def bar(self):
            return "baz"

    foo = Foo()
    foo.bar
    >>> "baz"
    ```
    """

    def __init__(self, _method: Callable[[T], R]) -> None:
        """
        Initialize the Kundera with a method.

        Args:
            _method (Callable[[T], R]): The method to be lazily initialized.
        """
        self._method = _method
        self.__set_name = False

    def __set_name__(self, owner: Type[T], name):
        """
        Set the name of the descriptor and create a LazyLock field in the owner class.

        Args:
            owner (Type[T]): The owner class.
            name (str): The name of the descriptor.
        """
        mangled_name = f"_{self.__class__.__name__}__{name}"
        owner.__annotations__[mangled_name] = LazyLock
        if not self.__set_name:
            setattr(
                owner,
                mangled_name,
                Field(
                    MISSING,
                    default_factory=functools.partial(LazyLock, self._method),
                    init=True,
                    repr=False,
                    hash=False,
                    compare=False,
                    metadata={},
                    kw_only=False,
                ),
            )
            self.__set_name = mangled_name

    @overload
    def __get__(self, instance: None, owner: Type[T]) -> Self: ...

    @overload
    def __get__(self, instance: T, owner: Type[T]) -> R: ...

    def __get__(self, instance: T | None, owner: Type[T]):
        """
        Get the value of the descriptor, initializing it if necessary.

        Args:
            instance (T | None): The instance of the owner class.
            owner (Type[T]): The owner class.

        Returns:
            The result of the method if instance is not None, otherwise the descriptor itself.
        """
        if instance is not None:
            lazy_lock: LazyLock[[T], R] = getattr(instance, self.__set_name)
            return lazy_lock(instance)
        return self
