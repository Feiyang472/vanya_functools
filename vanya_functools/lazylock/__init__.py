 from dataclasses import MISSING, Field
 import functools
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
     _NOT_FOUND = object()
 
     def __init__(self, callable: Callable[[P], R]) -> None:
         self.lock = Lock()
         self.callable = callable
         self.result = self.__class__._NOT_FOUND
 
     def __call__(self, *args: P.args, **kwargs: P.kwargs):
         val = self.result
         if val is self.__class__._NOT_FOUND:
             with self.lock:
                 # check if another thread filled cache while we awaited lock
                 val = self.result
                 if val is self.__class__._NOT_FOUND:
                     val = self.callable(*args, **kwargs)
                     self.result = val
         return val
 
 
 class SpecialDescriptor(Generic[T, R]):
     def __init__(self, _method: Callable[[T], R]) -> None:
         self._method = _method
         self.__set_name = False
 
     def __set_name__(self, owner: Type[T], name):
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
         if instance is not None:
             lazy_lock: LazyLock[[T], R] = getattr(
                 instance, self.__set_name
             )
             return lazy_lock(instance)
         else:
             return self