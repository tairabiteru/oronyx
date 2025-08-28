import datetime
import oronyx


def test_function_resolver():
    test_str = "in 6 days"
    function = oronyx.get_scheduler(test_str)
    assert function.name == "in_timedelta"


def test_offset():
    now = datetime.datetime(2025, 2, 4, 18, 0, 0)
    future = oronyx.get_future(now, "in 3 hours")
    assert future == datetime.datetime(2025, 2, 4, 21, 0, 0)