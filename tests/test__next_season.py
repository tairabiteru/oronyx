import datetime
import oronyx
import zoneinfo


def test_function_resolver():
    timeline = oronyx.get_blank_timeline("next spring")
    assert timeline is not None
    assert timeline.determinant.__name__ == "next_season"


def test_before():
    now = datetime.datetime(2025, 1, 4, 11, 45, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))
    timeline = oronyx.get_timeline(now, "next spring")
    assert timeline[0] == datetime.datetime(2025, 3, 20, 9, 1, 26, 759182, tzinfo=zoneinfo.ZoneInfo("UTC"))


def test_after():
    now = datetime.datetime(2025, 3, 25, 11, 45, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))
    timeline = oronyx.get_timeline(now, "next spring")
    assert timeline[0] == datetime.datetime(2026, 3, 20, 14, 45, 36, 44423, tzinfo=zoneinfo.ZoneInfo("UTC"))