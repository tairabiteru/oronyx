import datetime
import oronyx


def test_function_resolver():
    timeline = oronyx.get_blank_timeline("2 days before the last day of the month at 12:00")
    assert timeline is not None
    assert timeline.determinant.__name__ == "timedelta_before_the_last_day_of_the_month_at_time"


def test_last_day():
    now = datetime.datetime(2025, 9, 3, 17, 0, 0)
    timeline = oronyx.get_timeline(now, "2 days before the last day of the month")
    assert timeline[-1] == datetime.datetime(2025, 8, 29, 0, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 9, 28, 0, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 10, 29, 0, 0, 0)


def test_same_day_before():
    now = datetime.datetime(2025, 9, 23, 0, 0, 0)
    timeline = oronyx.get_timeline(now, "1 week before the last day of the month at 2:00")
    assert timeline[-1] == datetime.datetime(2025, 8, 24, 2, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 9, 23, 2, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 10, 24, 2, 0, 0)


def test_same_day_after():
    now = datetime.datetime(2025, 9, 23, 23, 0, 0)
    timeline = oronyx.get_timeline(now, "1 week before the last day of the month at 2:00")
    assert timeline[-1] == datetime.datetime(2025, 9, 23, 2, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 10, 24, 2, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 11, 23, 2, 0, 0)