import unittest

from more_peekable import Peekable

less_than_five = lambda n: n < 5


class PeekableTestCase(unittest.TestCase):
    def setUp(self):
        self.range = Peekable(range(10))

    def test_next_if(self):
        assert self.range.next_if(less_than_five) == 0
        for i in self.range:
            if not less_than_five(i):
                break
        assert self.range.next_if(less_than_five) is None

    def test_next_if_eq(self):
        assert self.range.next_if_eq(0) == 0
        assert self.range.next_if_eq(0) is None

    def test_take_while(self):
        assert list(self.range.take_while(less_than_five)) == [0, 1, 2, 3, 4]
        assert next(self.range) == 5
        assert list(self.range) == [6, 7, 8, 9]
