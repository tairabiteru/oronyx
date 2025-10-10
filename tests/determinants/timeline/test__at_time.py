import datetime
import oronyx


def test_function_resolver():
    timeline = oronyx.get_blank_timeline("at 3:45")
    assert timeline is not None
    assert timeline.determinant.__name__ == "at_time"


def test_before():
    now = datetime.datetime(2025, 2, 4, 11, 45, 0)
    timeline = oronyx.get_timeline(now, "at 11:46")
    assert timeline[0] == datetime.datetime(2025, 2, 4, 11, 46, 0)


def test_after():
    now = datetime.datetime(2025, 2, 4, 11, 46, 0)
    timeline = oronyx.get_timeline(now, "at 11:46")
    assert timeline[0] == datetime.datetime(2025, 2, 5, 11, 46, 0)