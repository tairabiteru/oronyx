import datetime
import oronyx


def test_function_resolver():
    timeline = oronyx.get_blank_timeline("on the last tuesday of the month at 16:30")
    assert timeline is not None
    assert timeline.determinant.__name__ == "on_the_last_weekday_of_the_month_at_time"


def test_before():
    now = datetime.datetime(2025, 8, 2, 12, 0, 0)
    timeline = oronyx.get_timeline(now, "on the last saturday of the month at 13:00")
    assert timeline[-1] == datetime.datetime(2025, 7, 26, 13, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 8, 30, 13, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 9, 27, 13, 0, 0)


def test_after():
    now = datetime.datetime(2025, 8, 30, 13, 0, 1)
    timeline = oronyx.get_timeline(now, "on the last saturday of the month at 13:00")
    assert timeline[-1] == datetime.datetime(2025, 8, 30, 13, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 9, 27, 13, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 10, 25, 13, 0, 0)