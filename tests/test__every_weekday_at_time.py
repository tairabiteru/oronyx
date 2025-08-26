import datetime
import oronyx


def test_function_resolver():
    test_str = "every tuesday"
    function = oronyx.get_scheduler(test_str)
    assert function.name == "every_weekday_at_time"


def test_weekday():
    now = datetime.datetime(2025, 8, 20, 17, 0, 0)
    future = oronyx.get_future(now, "every tuesday")
    assert future == datetime.datetime(2025, 8, 26, 0, 0, 0)


def test_weekday_same_day_before():
    now = datetime.datetime(2025, 8, 26, 17, 0, 0)
    future = oronyx.get_future(now, "every tuesday at 23:00")
    assert future == datetime.datetime(2025, 8, 26, 23, 0, 0)


def test_weekday_same_day_after():
    now = datetime.datetime(2025, 8, 26, 17, 0, 0)
    future = oronyx.get_future(now, "every tuesday at 2:00")
    assert future == datetime.datetime(2025, 9, 2, 2, 0, 0)


def test_end_of_year():
    now = datetime.datetime(2025, 12, 31, 23, 0, 0)
    future = oronyx.get_future(now, "every friday at 9:00")
    assert future == datetime.datetime(2026, 1, 2, 9, 0, 0)