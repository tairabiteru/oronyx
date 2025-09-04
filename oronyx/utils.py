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