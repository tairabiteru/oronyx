import datetime
import oronyx


def test_function_resolver():
    timeline = oronyx.get_blank_timeline("in 6 days")
    assert timeline is not None
    assert timeline.determinant.__name__ == "in_timedelta"


def test_before():
    now = datetime.datetime(2025, 2, 4, 11, 45, 0)
    timeline = oronyx.get_timeline(now, "at 11:46")
    assert timeline[0] == datetime.datetime(2025, 2, 4, 11, 46, 0)


def test_after():
    now = datetime.datetime(2025, 2, 4, 11, 46, 0)
    timeline = oronyx.get_timeline(now, "at 11:46")
    assert timeline[0] == datetime.datetime(2025, 2, 5, 11, 46, 0)