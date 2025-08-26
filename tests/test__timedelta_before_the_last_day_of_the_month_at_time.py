import datetime
import oronyx


def test_function_resolver():
    test_str = "2 days before the last day of the month at 12:00"
    function = oronyx.get_scheduler(test_str)
    assert function.name == "timedelta_before_the_last_day_of_the_month_at_time"


def test_last_day():
    now = datetime.datetime(2025, 9, 3, 17, 0, 0)
    future = oronyx.get_future(now, "2 days before the last day of the month")
    assert future == datetime.datetime(2025, 9, 28, 0, 0, 0)


def test_same_day_before():
    now = datetime.datetime(2025, 9, 23, 0, 0, 0)
    future = oronyx.get_future(now, "1 week before the last day of the month at 2:00")
    assert future == datetime.datetime(2025, 9, 23, 2, 0, 0)


def test_same_day_after():
    now = datetime.datetime(2025, 9, 23, 23, 0, 0)
    future = oronyx.get_future(now, "1 week before the last day of the month at 2:00")
    assert future == datetime.datetime(2025, 10, 24, 2, 0, 0)


def test_leap_year():
    now = datetime.datetime(2024, 2, 2, 18, 30, 0)
    future = oronyx.get_future(now, "8 days before the last day of the month at 22:45")
    assert future == datetime.datetime(2024, 2, 21, 22, 45, 0)


def test_non_leap_year():
    now = datetime.datetime(2025, 2, 2, 18, 30, 0)
    future = oronyx.get_future(now, "8 days before the last day of the month at 22:45")
    assert future == datetime.datetime(2025, 2, 20, 22, 45, 0)