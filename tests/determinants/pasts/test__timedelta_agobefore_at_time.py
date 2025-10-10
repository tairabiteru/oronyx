import datetime
import oronyx


def test_function_resolver():
    past = oronyx.get_past_obj("2 days ago")
    assert isinstance(past, oronyx.impl.Past)
    assert past.name == "timedelta_agobefore_at_time"