import datetime
import oronyx


def test_function_resolver():
    test_str = "2 days before"
    function = oronyx.get_delta_determiner(test_str)
    assert function.name == "timedelta_before"


def test_before():
    now = datetime.datetime(2003, 1, 6, 0, 0, 0)
    delta = oronyx.get_delta(now, "2 days before")
    assert delta == datetime.datetime(2003, 1, 4, 0, 0, 0)


def test_after():
    now = datetime.datetime(2003, 1, 7, 0, 0, 0)
    delta = oronyx.get_delta(now, "2 weeks after")
    assert delta == datetime.datetime(2003, 1, 21, 0, 0, 0)