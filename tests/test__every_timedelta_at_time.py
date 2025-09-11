import datetime
import oronyx


def test_function_resolver():
    timeline = oronyx.get_blank_timeline("every 2 days at 12:00")
    assert timeline is not None
    assert timeline.determinant.__name__ == "every_timedelta_at_time"


def test_timedelta():
    now = datetime.datetime(2025, 8, 1, 0, 0, 0)
    timeline = oronyx.get_timeline(now, "every 2 days")
    assert timeline[-1] == datetime.datetime(2025, 8, 1, 0, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 8, 3, 0, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 8, 5, 0, 0, 0)


def test_timedelta_time():
    now = datetime.datetime(2025, 12, 7, 9, 0, 0)
    timeline = oronyx.get_timeline(now, "every 9 days at 7:32")
    assert timeline[-2] == datetime.datetime(2025, 11, 28, 7, 32, 0)
    assert timeline[-1] == datetime.datetime(2025, 12, 7, 7, 32, 0)
    assert timeline[0] == datetime.datetime(2025, 12, 16, 7, 32, 0)
    assert timeline[1] == datetime.datetime(2025, 12, 25, 7, 32, 0)


def test_end_of_year():
    now = datetime.datetime(2025, 12, 30, 23, 0, 0)
    timeline = oronyx.get_timeline(now, "every 3 days at 0:00")
    assert timeline[0] == datetime.datetime(2026, 1, 2, 0, 0, 0)