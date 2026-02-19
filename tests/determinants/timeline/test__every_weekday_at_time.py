import datetime
import oronyx


def test_function_resolver_every():
    timeline = oronyx.get_blank_timeline("every tuesday")
    assert timeline is not None
    assert timeline.determinant.__name__ == "every_weekday_at_time"


def test_weekday():
    now = datetime.datetime(2025, 8, 20, 17, 0, 0)
    timeline = oronyx.get_timeline(now, "every tuesday")
    assert timeline[0] == datetime.datetime(2025, 8, 26, 0, 0, 0)


def test_weekday_same_day_before():
    now = datetime.datetime(2025, 8, 26, 17, 0, 0)
    timeline = oronyx.get_timeline(now, "every tuesday at 23:00")
    assert timeline[-1] == datetime.datetime(2025, 8, 19, 23, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 8, 26, 23, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 9, 2, 23, 0, 0)


def test_weekday_same_day_after():
    now = datetime.datetime(2025, 8, 26, 17, 0, 0)
    timeline = oronyx.get_timeline(now, "every tuesday at 2:00")
    assert timeline[-1] == datetime.datetime(2025, 8, 26, 2, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 9, 2, 2, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 9, 9, 2, 0, 0)


def test_end_of_year():
    now = datetime.datetime(2025, 12, 31, 23, 0, 0)
    timeline = oronyx.get_timeline(now, "every friday at 9:00")
    assert timeline[0] == datetime.datetime(2026, 1, 2, 9, 0, 0)
    

def test_function_resolver_on():
    timeline = oronyx.get_blank_timeline("on Monday at 9:00 AM")
    assert timeline is not None
    assert timeline.determinant.__name__ == "every_weekday_at_time"


def test_on_weekday():
    now = datetime.datetime(2025, 8, 26, 17, 0, 0)
    timeline = oronyx.get_timeline(now, "on monday")
    assert timeline[-1] == datetime.datetime(2025, 8, 25, 0, 0, 0)
    assert timeline[0] == datetime.datetime(2025, 9, 1, 0, 0, 0)
    assert timeline[1] == datetime.datetime(2025, 9, 8, 0, 0, 0)


def test_on_weekday_at_time():
    now = datetime.datetime(2026, 2, 8, 6, 0, 0)
    timeline = oronyx.get_timeline(now, "on Monday at 9:00 AM")
    assert timeline[-1] == datetime.datetime(2026, 2, 2, 9, 0, 0)
    assert timeline[0] == datetime.datetime(2026, 2, 9, 9, 0, 0)
    assert timeline[1] == datetime.datetime(2026, 2, 16, 9, 0, 0)