import pytest

def get_values():
    return [ 0, 1, 2, 3, 4, 5 ]

def even_case_name(value):
    return "custom_" + str(value)

@pytest.mark.parametrize("i", get_values(), ids=even_case_name)
def test_even(i):
    assert i % 2 == 0

def a_case_name(value):
    return "a_" + str(value)

def b_case_name(value):
    return "b_" + str(value)

@pytest.mark.parametrize("i", get_values(), ids=a_case_name)
@pytest.mark.parametrize("j", get_values(), ids=b_case_name)
def test_equals_stacked(i, j):
    assert i == j
