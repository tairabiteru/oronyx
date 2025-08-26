import datetime
import oronyx


def test_function_resolver():
    test_str = "every 2 days at 12:00"
    function = oronyx.get_scheduler(test_str)
    assert function.name == "every_timedelta_at_time"


def test_timedelta():
    now = datetime.datetime(2025, 8, 1, 0, 0, 0)
    future = oronyx.get_future(now, "every 2 days")
    assert future == datetime.datetime(2025, 8, 3, 0, 0, 0)


def test_timedelta_time():
    now = datetime.datetime(2025, 12, 7, 9, 0, 0)
    future = oronyx.get_future(now, "every 9 days at 7:32")
    assert future == datetime.datetime(2025, 12, 16, 7, 32, 0)


def test_end_of_year():
    now = datetime.datetime(2025, 12, 30, 23, 0, 0)
    future = oronyx.get_future(now, "every 3 days at 0:00")
    assert future == datetime.datetime(2026, 1, 2, 0, 0, 0)