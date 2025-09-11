from oronyx.tokens import TimeDelta


def test_seconds():
    assert TimeDelta("12 seconds").delta.total_seconds() == 12
    assert TimeDelta("1 second").delta.total_seconds() == 1


def test_minutes():
    assert TimeDelta("35 minutes").delta.total_seconds() == (60 * 35)
    assert TimeDelta("1 minute").delta.total_seconds() == (60 * 1)


def test_hours():
    assert TimeDelta("19 hours").delta.total_seconds() == (3600 * 19)
    assert TimeDelta("1 hour").delta.total_seconds() == (3600 * 1)


def test_days():
    assert TimeDelta("90 days").delta.total_seconds() == (86400 * 90)
    assert TimeDelta("1 day").delta.total_seconds() == (86400 * 1)


def test_weeks():
    assert TimeDelta("36 weeks").delta.total_seconds() == ((7 * 86400) * 36)
    assert TimeDelta("1 week").delta.total_seconds() == ((7 * 86400) * 1)


def test_years():
    assert TimeDelta("87 years").delta.total_seconds() == ((365 * 86400) * 87)
    assert TimeDelta("1 year").delta.total_seconds() == ((365 * 86400) * 1)