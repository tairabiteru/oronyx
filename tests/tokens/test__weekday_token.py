from oronyx.tokens import Weekday


def test_weekday():
    assert Weekday("monday").number == 0
    assert Weekday("tuesdays").number == 1
    assert Weekday("wednesdays").number == 2
    assert Weekday("thursday").number == 3
    assert Weekday("fridays").number == 4
    assert Weekday("saturday").number == 5
    assert Weekday("sundays").number == 6