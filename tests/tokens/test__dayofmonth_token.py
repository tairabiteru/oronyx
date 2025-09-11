from oronyx.tokens import DayOfMonth


def test_dayofmonth():
    assert DayOfMonth("day 1").day == 1
    assert DayOfMonth("day 31").day == 31
    
    try:
        DayOfMonth("day 32")
    except ValueError as e:
        assert str(e) == "Months can't have more than 31 days."