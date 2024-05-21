"""
Extends the peekable class from more-itertools.

```py
from more_itertools import Peekable
```
"""

__name__ = "more_peekable"
__author__ = "Ernie Izdebski"
__description__ = "Extends the peekable class from more-itertools"
__copyright__ = "Copyright 2024-present Ernie Izdebski"
__license__ = "MIT"
__url__ = "https://github.com/ernieIzde8ski/more-itertools"
__version__ = "0.1.0"

__all__ = ["Peekable"]

from typing import TYPE_CHECKING, Any, Callable, Generic, Iterable, TypeVar, overload

T = TypeVar("T")
U = TypeVar("U")


if TYPE_CHECKING:
    from more_itertools import peekable as PeekableBase
else:
    from more_itertools import peekable

    class PeekableBase(peekable, Generic[T]):
        pass


callback = Callable[[T], Any]


class Peekable(PeekableBase[T]):
    @overload
    def next_if(self, func: callback) -> T | None: ...

    @overload
    def next_if(self, func: callback, default: U) -> T | U: ...

    def next_if(self, func, default=None):
        """Consume and return the next value of this iterator if a condition is true.

        If `func` is true-ish for the next value of this iterator, consume and return it.
        Otherwise, return the default.

        ## Examples

        Consume a number if it's equal to 0.

        ```python
        numbers = Peekable(range(5))
        assert iterator.next_if(lambda n: n == 0) == 0
        assert iterator.next_if(lambda n: n == 0) is None
        assert next(iterator) == 1
        ```

        Consume any number less than ten.

        ```python
        numbers = Peekable(range(1, 20))
        while numbers.next_if(lambda n: n < 10) is not None:
            pass
        assert next(numbers) == 10
        ```
        """
        if not self:
            return default
        if not func(self.peek()):
            return default
        return next(self)

    @overload
    def next_if_eq(self, expected: T) -> T | None: ...

    @overload
    def next_if_eq(self, expected: T, default: U) -> T | U: ...

    def next_if_eq(self, expected, default=None):
        """Consume and return the next item if it is equal to expected.

        ## Example

        Consume a number if it's equal to 0.

        ```python
        numbers = Peekable(range(5))
        assert numbers.next_if_eq(0) == 0
        assert numbers.next_if_eq(0) is None
        assert next(numbers) is None
        ```
        """

        if not self:
            return default
        if self.peek() != expected:
            return default
        return next(self)

    def take_while(self, func: callback) -> Iterable[T]:
        while self:
            if func(self.peek()):
                yield next(self)
            else:
                break
