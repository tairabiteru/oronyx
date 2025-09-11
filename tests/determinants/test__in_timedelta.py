import datetime
import oronyx


def test_function_resolver():
    timeline = oronyx.get_blank_timeline("in 6 days")
    assert timeline is not None
    assert timeline.determinant.__name__ == "in_timedelta"


def test_offset():
    now = datetime.datetime(2025, 2, 4, 18, 0, 0)
    timeline = oronyx.get_timeline(now, "in 3 hours")
    assert timeline[-1] == datetime.datetime(2025, 2, 4, 15, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 2, 4, 21, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 2, 5, 0, 0, 0)