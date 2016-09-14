import unittest

class NumbersTest(unittest.TestCase):

    def test_even(self):
        for i in range(0, 6):
            yield self.is_even, i

    def is_even(self, i):
        self.assertEquals(i % 2, 0)
