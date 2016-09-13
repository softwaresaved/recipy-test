import pytest

@pytest.mark.parametrize("i", [0, 1, 2, 3, 4, 5])
def test_even(i):
    assert i % 2 == 0
