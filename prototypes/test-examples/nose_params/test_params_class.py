import unittest
from nose_parameterized import parameterized

class NumbersTest(unittest.TestCase):

    @parameterized.expand([ (0,), (1,), (2,), (3,), (4,), (5,)  ])
    def test_even(self, i):
        self.assertEquals(i % 2, 0)
