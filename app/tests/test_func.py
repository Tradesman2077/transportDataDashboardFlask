import pytest
# some function we want to test
def inc(x):
    return x + 1
# a function which tests inc()
def test_inc():
    assert inc(3) == 4