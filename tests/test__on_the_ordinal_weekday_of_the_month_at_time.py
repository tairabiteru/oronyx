import datetime
import oronyx


def test_function_resolver():
    test_str = "on the 3rd tuesday of the month at 16:30"
    function = oronyx.get_scheduler(test_str)
    assert function.name == "on_the_ordinal_weekday_of_the_month_at_time"


def test_same_day_before():
    now = datetime.datetime(2025, 8, 2, 12, 0, 0)
    future = oronyx.get_future(now, "on the 1st saturday of the month at 13:00")
    assert future == datetime.datetime(2025, 8, 2, 13, 0, 0)


def test_same_day_after():
    now = datetime.datetime(2025, 8, 2, 13, 0, 1)
    future = oronyx.get_future(now, "on the 1st saturday of the month at 13:00")
    assert future == datetime.datetime(2025, 9, 6, 13, 0, 0)


def test_error():
    now = datetime.datetime(2025, 9, 23, 23, 0, 0)
    try:
        _ = oronyx.get_future(now, "on the 9th saturday of the month")
    except ValueError as e:
        assert str(e) == "Invalid ordinal for 9/2025: '9'. There is no 9th saturday of that month."


def test_3rd_tuesday():
    now = datetime.datetime(2025, 1, 8, 18, 30, 0)
    future = oronyx.get_future(now, "on the 3rd tuesday of the month")
    assert future == datetime.datetime(2025, 1, 21, 0, 0, 0)