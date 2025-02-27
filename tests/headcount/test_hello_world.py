from src.headcount.hello_world import say_hi


def test_hi():
    assert isinstance(say_hi(), str)
