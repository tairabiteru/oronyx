import datetime
import oronyx


def test_function_resolver():
    timeline = oronyx.get_blank_timeline("next meteorological summer")
    assert timeline is not None
    assert timeline.determinant.__name__ == "next_meteorological_season"


def test_before():
    now = datetime.datetime(2025, 1, 4, 11, 45, 0)
    timeline = oronyx.get_timeline(now, "next meteorological summer")
    assert timeline[-1] == datetime.datetime(2024, 6, 1)
    assert timeline[0] == datetime.datetime(2025, 6, 1)
    assert timeline[1] == datetime.datetime(2026, 6, 1)


def test_after():
    now = datetime.datetime(2025, 6, 4, 11, 45, 0)
    timeline = oronyx.get_timeline(now, "next meteorological summer")
    assert timeline[-1] == datetime.datetime(2025, 6, 1)
    assert timeline[0] == datetime.datetime(2026, 6, 1)
    assert timeline[1] == datetime.datetime(2027, 6, 1)