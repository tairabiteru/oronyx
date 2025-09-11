import datetime
import oronyx


def test_function_resolver():
    timeline = oronyx.get_blank_timeline("on day 12 of each month at 17:21")
    assert timeline is not None
    assert timeline.determinant.__name__ == "on_dayofmonth_of_each_month_at_time"


def test_before():
    now = datetime.datetime(2025, 2, 4, 18, 0, 0)
    timeline = oronyx.get_timeline(now, "on day 7 of each month")
    assert timeline[-1] == datetime.datetime(2025, 1, 7, 0, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 2, 7, 0, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 3, 7, 0, 0, 0)


def test_after():
    now = datetime.datetime(2025, 11, 23, 0, 0, 0)
    timeline = oronyx.get_timeline(now, "on day 5 of each month")
    assert timeline[-1] == datetime.datetime(2025, 11, 5, 0, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 12, 5, 0, 0, 0)
    assert timeline[1] == datetime.datetime(2026, 1, 5, 0, 0, 0)


def test_same_day_before():
    now = datetime.datetime(2025, 1, 2, 10, 30, 0)
    timeline = oronyx.get_timeline(now, "on day 2 of each month at 12:00")
    assert timeline[-1] == datetime.datetime(2024, 12, 2, 12, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 1, 2, 12, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 2, 2, 12, 0, 0)


def test_same_day_after():
    now = datetime.datetime(2025, 1, 2, 10, 30, 0)
    timeline = oronyx.get_timeline(now, "on day 2 of each month at 9:00")
    assert timeline[-1] == datetime.datetime(2025, 1, 2, 9, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 2, 2, 9, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 3, 2, 9, 0, 0)