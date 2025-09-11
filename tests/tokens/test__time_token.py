import datetime
from oronyx.tokens import Time


def test_24h():
    assert Time("12:00").time == datetime.time(12)
    assert Time("13").time == datetime.time(13)
    assert Time("23:59:59").time == datetime.time(23, 59, 59)


def test_12h():
    assert Time("12 PM").time == datetime.time(12)
    assert Time("9:00 am").time == datetime.time(9, 0)
    assert Time("1 PM").time == datetime.time(13)
    assert Time("11:25:39 PM").time == datetime.time(23, 25, 39)