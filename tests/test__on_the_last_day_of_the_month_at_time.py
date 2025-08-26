import datetime
import oronyx


def test_function_resolver():
    test_str = "on the last day of the month at 12:00"
    function = oronyx.get_scheduler(test_str)
    assert function.name == "on_the_last_day_of_the_month_at_time"


def test_last_day():
    now = datetime.datetime(2025, 9, 3, 17, 0, 0)
    future = oronyx.get_future(now, "on the last day of the month")
    assert future == datetime.datetime(2025, 9, 30, 0, 0, 0)


def test_same_day_before():
    now = datetime.datetime(2025, 9, 30, 0, 0, 0)
    future = oronyx.get_future(now, "on the last day of the month at 2:00")
    assert future == datetime.datetime(2025, 9, 30, 2, 0, 0)


def test_same_day_after():
    now = datetime.datetime(2025, 9, 30, 23, 0, 0)
    future = oronyx.get_future(now, "on the last day of the month at 2:00")
    assert future == datetime.datetime(2025, 10, 31, 2, 0, 0)


def test_leap_year():
    now = datetime.datetime(2024, 2, 2, 18, 30, 0)
    future = oronyx.get_future(now, "on the last day of the month at 22:45")
    assert future == datetime.datetime(2024, 2, 29, 22, 45, 0)


def test_non_leap_year():
    now = datetime.datetime(2025, 2, 2, 18, 30, 0)
    future = oronyx.get_future(now, "on the last day of the month at 22:45")
    assert future == datetime.datetime(2025, 2, 28, 22, 45, 0)


def test_end_of_year_before():
    now = datetime.datetime(2025, 12, 31, 18, 30, 0)
    future = oronyx.get_future(now, "on the last day of the month at 22:45")
    assert future == datetime.datetime(2025, 12, 31, 22, 45, 0)


def test_end_of_year_after():
    now = datetime.datetime(2025, 12, 31, 18, 30, 0)
    future = oronyx.get_future(now, "on the last day of the month at 5:45")
    assert future == datetime.datetime(2026, 1, 31, 5, 45, 0)