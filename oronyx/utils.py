import datetime


def get_last_day_of_month(month: int, year: int) -> int:
    """
    Given the month and year, get the last day of the month.

    This will return the 29th of February on leap years.
    
    
    """
    LAST_DAYS = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2:
        try:
            datetime.datetime(year, 2, 29, 0, 0, 0)
            return 29
        except ValueError:
            return 28
    else:
        return LAST_DAYS[month]
