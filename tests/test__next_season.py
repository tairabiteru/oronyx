import datetime
import oronyx
import zoneinfo


def test_function_resolver():
    test_str = "next spring"
    function = oronyx.get_scheduler(test_str)
    assert function.name == "next_season"


def test_before():
    now = datetime.datetime(2025, 1, 4, 11, 45, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))
    future = oronyx.get_future(now, "next spring")
    future = future.replace(microsecond=0)
    assert future == datetime.datetime(2025, 3, 20, 9, 1, 26, tzinfo=zoneinfo.ZoneInfo("UTC"))


def test_after():
    now = datetime.datetime(2025, 3, 21, 11, 45, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))
    future = oronyx.get_future(now, "next spring")
    future = future.replace(microsecond=0)
    assert future == datetime.datetime(2026, 3, 20, 14, 45, 36, tzinfo=zoneinfo.ZoneInfo("UTC"))