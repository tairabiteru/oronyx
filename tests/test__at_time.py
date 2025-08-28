import datetime
import oronyx


def test_function_resolver():
    test_str = "in 6 days"
    function = oronyx.get_scheduler(test_str)
    assert function.name == "in_timedelta"


def test_before():
    now = datetime.datetime(2025, 2, 4, 11, 45, 0)
    future = oronyx.get_future(now, "at 11:46")
    assert future == datetime.datetime(2025, 2, 4, 11, 46, 0)