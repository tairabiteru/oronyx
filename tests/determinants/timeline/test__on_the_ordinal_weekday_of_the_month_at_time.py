import datetime
import oronyx


def test_function_resolver():
    timeline = oronyx.get_blank_timeline("on the 3rd tuesday of the month at 16:30")
    assert timeline is not None
    assert timeline.determinant.__name__ == "on_the_ordinal_weekday_of_the_month_at_time"


def test_same_day_before():
    now = datetime.datetime(2025, 8, 2, 12, 0, 0)
    timeline = oronyx.get_timeline(now, "on the 1st saturday of the month at 13:00")
    assert timeline[-1] == datetime.datetime(2025, 7, 5, 13, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 8, 2, 13, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 9, 6, 13, 0, 0)


def test_same_day_after():
    now = datetime.datetime(2025, 8, 2, 13, 0, 1)
    timeline = oronyx.get_timeline(now, "on the 1st saturday of the month at 13:00")
    assert timeline[-1] == datetime.datetime(2025, 8, 2, 13, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 9, 6, 13, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 10, 4, 13, 0, 0)


def test_error():
    now = datetime.datetime(2025, 9, 23, 23, 0, 0)
    try:
        _ = oronyx.get_timeline(now, "on the 5th saturday of the month")
    except ValueError:
        assert True