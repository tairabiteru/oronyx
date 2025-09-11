from astronomy import Seasons
import datetime
import zoneinfo


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


def month_step(step: int, month: int, year: int) -> tuple[int, int]:
    if step > 0:
        while step > 0:
            month += 1
            if month == 13:
                month = 1
                year += 1
            step -= 1
    elif step < 0:
        while step < 0:
            month -= 1
            if month == 0:
                month = 12
                year -= 1
            step += 1
    return month, year


def get_nth_weekday_of_month(month: int, year: int, ordinal: int, weekday: int) -> int | None:
    if ordinal > 5:
        raise ValueError("Ordinal argument cannot be greater than 5.")

    date = datetime.datetime(year, month, 1)
    while date.weekday() != weekday:
        date += datetime.timedelta(days=1)
    
    date = (date + datetime.timedelta(days=(7 * (ordinal  - 1))))

    if date.month != month:
        return None
    return date.day
    

def get_solar_event_for_year(year: int, season: str) -> datetime.datetime:
    seasons = Seasons(year)
    event = datetime.datetime(2000, 1, 1, 12, 0, 0, 0, zoneinfo.ZoneInfo("UTC"))

    match season:
        case "spring":
            event += datetime.timedelta(days=seasons.mar_equinox.ut)
        case "summer":
            event += datetime.timedelta(days=seasons.jun_solstice.ut)
        case "autumn":
            event += datetime.timedelta(days=seasons.sep_equinox.ut)
        case "winter":
            event += datetime.timedelta(days=seasons.dec_solstice.ut)
        case _:
            raise ValueError("This should never occur.")

    return event


def get_season(now: datetime.datetime) -> str:
    season = get_solar_event_for_year(now.year, "spring")
    if now < season:
        return "winter"
    
    season = get_solar_event_for_year(now.year, "summer")
    if now < season:
        return "spring"
    
    season = get_solar_event_for_year(now.year, "autumn")
    if now < season:
        return "summer"
    
    season = get_solar_event_for_year(now.year, "winter")
    if now < season:
        return "autumn"

    return "winter"


def last_weekday_eval(
    now: datetime.datetime,
    i: int,
    t_weekday,
    t_time,
    reference: datetime.datetime | None = None
) -> datetime.datetime:
    if reference is None:
        last_day = get_last_day_of_month(now.month, now.year)
        reference = now.replace(day=last_day, hour=t_time.hour, minute=t_time.minute, second=t_time.second, microsecond=0, tzinfo=now.tzinfo)
    else:
        last_day = get_last_day_of_month(reference.month, reference.year)
        reference = reference.replace(day=last_day)

    while reference.weekday() != t_weekday.number:
        reference -= datetime.timedelta(days=1)

    if i > 0:
        m, y = month_step(1, reference.month, reference.year)
        reference = reference.replace(year=y, month=m, day=1)
        return last_weekday_eval(now, i-1, t_weekday, t_time, reference=reference)
    elif i < 0:
        m, y = month_step(-1, reference.month, reference.year)
        reference = reference.replace(year=y, month=m, day=1)
        return last_weekday_eval(now, i+1, t_weekday, t_time, reference=reference)
    
    return reference


def ord_weekday_eval(
    now: datetime.datetime,
    i: int,
    t_ordinal,
    t_weekday,
    t_time,
    reference: datetime.datetime | None = None
) -> datetime.datetime:
    if t_ordinal.number > 4:
        raise ValueError("You cannot use ordinals greater than 4th.")

    if reference is None:
        nth_weekday = get_nth_weekday_of_month(now.month, now.year, t_ordinal.number, t_weekday.number)
        assert nth_weekday is not None
        reference = now.replace(day=nth_weekday, hour=t_time.hour, minute=t_time.minute, second=t_time.second, microsecond=0, tzinfo=now.tzinfo)
    else:
        nth_weekday = get_nth_weekday_of_month(reference.month, reference.year, t_ordinal.number, t_weekday.number)
        assert nth_weekday is not None
        reference = reference.replace(day=nth_weekday)

    if i > 0:
        m, y = month_step(1, reference.month, reference.year)
        reference = reference.replace(year=y, month=m, day=1)
        return ord_weekday_eval(now, i-1, t_ordinal, t_weekday, t_time, reference=reference)
    elif i < 0:
        m, y = month_step(-1, reference.month, reference.year)
        reference = reference.replace(year=y, month=m, day=1)
        return ord_weekday_eval(now, i+1, t_ordinal, t_weekday, t_time, reference=reference)

    return reference