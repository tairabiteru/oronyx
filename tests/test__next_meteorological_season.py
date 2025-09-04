import datetime
import oronyx


def test_function_resolver():
    test_str = "next meteorological summer"
    function = oronyx.get_scheduler(test_str)
    assert function.name == "next_meteorological_season"


def test_before():
    now = datetime.datetime(2025, 1, 4, 11, 45, 0)
    future = oronyx.get_future(now, "next meteorological summer")
    assert future == datetime.datetime(2025, 6, 1)


def test_after():
    now = datetime.datetime(2025, 6, 4, 11, 45, 0)
    future = oronyx.get_future(now, "next meteorological summer")
    assert future == datetime.datetime(2026, 6, 1)