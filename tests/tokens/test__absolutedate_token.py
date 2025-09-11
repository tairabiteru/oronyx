import datetime
from oronyx.tokens import AbsoluteDate


def test_abs_date():
    assert AbsoluteDate("1/6/1994").date == datetime.date(1994, 1, 6)
    assert AbsoluteDate("01/06/1994").date == datetime.date(1994, 1, 6)
    assert AbsoluteDate("12/25/1963").date == datetime.date(1963, 12, 25)