def test_even():
    for i in range(0, 6):
        yield is_even, i

def is_even(i):
    assert i % 2 == 0
