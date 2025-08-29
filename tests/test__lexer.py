import datetime
from oronyx.decorators import lex
from oronyx.tokens import TimeDelta, Time, AnnualDate


def test_timedelta():
    test_str = "in 6 days at 4:30"
    tokens = lex(test_str)
    assert len(tokens) == 2
    assert isinstance(tokens[1], TimeDelta)
    assert tokens[1].delta.total_seconds() == (86400 * 6)


def test_time():
    test_str = "in 6 days at 4:30"
    tokens = lex(test_str)
    assert len(tokens) == 2
    assert isinstance(tokens[0], Time)
    assert tokens[0].hour == 4
    assert tokens[0].minute == 30
    assert tokens[0].second == 0
    assert tokens[0].time == datetime.time(4, 30, 0)


def test_annualdate():
    test_str = "on 7/4 at 19:30"
    tokens = lex(test_str)
    assert len(tokens) == 2
    assert isinstance(tokens[0], AnnualDate)
    assert tokens[0].day == 4
    assert tokens[0].month == 7
    assert tokens[0].month_name == "July"

