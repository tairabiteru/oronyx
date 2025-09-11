from oronyx.tokens import Ordinal


def test_weekday():
    assert Ordinal("1st").number == 1
    assert Ordinal("2nd").number == 2
    assert Ordinal("3rd").number == 3
    assert Ordinal("4th").number == 4
    assert Ordinal("5th").number == 5
    assert Ordinal("6th").number == 6
    assert Ordinal("7th").number == 7
    assert Ordinal("8th").number == 8
    assert Ordinal("9th").number == 9
    assert Ordinal("10th").number == 10
    assert Ordinal("21st").number == 21
    assert Ordinal("32nd").number == 32
    assert Ordinal("143rd").number == 143