# more-peekable

An extension of the `peekable` class from `more-itertools`. Adds
methods from Rust's `peekable` struct, easier support for subscripted
type annotations, and another dependency to your project.

## Usage

Install with `pip install more-peekable`.

```py
from more_peekable import Peekable

less_than_five = lambda n: n < 5

numbers = Peekable(range(10))

# Read every number up through five, without consuming the last
for number in numbers.take_while(less_than_five):
    assert number < 5
# Check the next number without consuming it
assert numbers.peek() == 5
# Check before consuming the next number, 5
assert numbers.next_if_eq(5) is not None
# Consume the next number, 6,
assert next(numbers) == 6
```

## Contributing

```sh
pip install -r requirements-dev.txt
pre-commit install
```

See Makefile for build process.
