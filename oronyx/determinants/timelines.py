import datetime

from ..impl import timeline
from ..tokens import TimeDelta, Time, Weekday, AnnualDate, DayOfMonth, Ordinal, Season
from ..utils import get_last_day_of_month, month_step, get_solar_event_for_year, get_nth_weekday_of_month, ord_weekday_eval, last_weekday_eval


@timeline(f"every {TimeDelta}( at {Time})?")
def every_timedelta_at_time(
    now: datetime.datetime, 
    i: int,
    t_delta: TimeDelta,
    t_time: Time | None = None
) -> datetime.datetime:
    if t_time is not None:
        reference = now.replace(hour=t_time.hour, minute=t_time.minute, second=t_time.second, microsecond=0)
    else:
        reference = now.replace(microsecond=0)
    
    if reference <= now:
        return reference + (t_delta.delta * (i + 1))
    else:
        return reference + (t_delta.delta * i)


@timeline(f"every ?day( at {Time})?")
def every_day_at_time(
    now: datetime.datetime, 
    i: int,
    t_time: Time | None = None
) -> datetime.datetime:
    return every_timedelta_at_time(now, i, TimeDelta("1 day"), t_time)


@timeline(f"at {Time}")
def at_time(
    now: datetime.datetime, 
    i: int,
    t_time: Time | None = None
) -> datetime.datetime:
    return every_timedelta_at_time(now, i, TimeDelta("1 day"), t_time)


@timeline(f"(every)|(on) {Weekday}( at {Time})?")
def every_weekday_at_time(
        now: datetime.datetime,
        i: int,
        t_weekday: Weekday, 
        t_time: Time = Time("00:00")
) -> datetime.datetime:
    """
    Schedule every {weekday} at {time}?

    Ex:
    every tuesday at 8:30
    every friday
    """
    reference = now.replace(hour=t_time.hour, minute=t_time.minute, second=t_time.second, microsecond=0)

    while reference.weekday() != t_weekday.number:
        reference += datetime.timedelta(days=1)

    if reference <= now:
        return reference + datetime.timedelta(days=7 * (i + 1))
    else:
        return reference + datetime.timedelta(days=7 * i)


@timeline(f"on the last day of the month( at {Time})?")
def on_the_last_day_of_the_month_at_time(
        now: datetime.datetime,
        i: int,
        t_time: Time = Time("00:00")
) -> datetime.datetime:
    """
    Schedule on the last day of the month at {time}?

    On leap years, this will return the 29th of February.

    Ex:
    on the last day of the month
    on the last day of the month at 23:59
    """
    # I don't like this because it violates DRY kind of
    # But I also spent like, 3 hours writing this.
    m, y = month_step(0, now.month, now.year)
    d = get_last_day_of_month(m, y)
    reference = datetime.datetime(y, m, d, t_time.hour, t_time.minute, t_time.second, 0, now.tzinfo)

    if now >= reference:
        m, y = month_step(i+1, now.month, now.year)
        d = get_last_day_of_month(m, y)
        next_instance = datetime.datetime(y, m, d, t_time.hour, t_time.minute, t_time.second, 0, now.tzinfo)
    else:
        m, y = month_step(i, now.month, now.year)
        d = get_last_day_of_month(m, y)
        next_instance = datetime.datetime(y, m, d, t_time.hour, t_time.minute, t_time.second, 0, now.tzinfo)

    return next_instance


@timeline(f"{TimeDelta} before the last day of the month( at {Time})?")
def timedelta_before_the_last_day_of_the_month_at_time(
    now: datetime.datetime,
    i: int,
    t_delta: TimeDelta,
    t_time: Time | None = Time("00:00")
) -> datetime.datetime:
    """
    Schedule {timedelta} beofre the last day of the month at {time}?

    Similar to "on the last day of the month" but an offset can be
    applied to it.

    Ex:
    2 days before the last day of the month
    2 weeks before the last day of the month at 8:30
    """
    target = on_the_last_day_of_the_month_at_time(now, 0, t_time)

    if (target - t_delta.delta) <= now:
        target = on_the_last_day_of_the_month_at_time(now, i+1, t_time)
    else:
        target = on_the_last_day_of_the_month_at_time(now, i, t_time)

    return target - t_delta.delta


@timeline(f"every year on {AnnualDate}( at {Time})?")
def every_year_on_annualdate_at_time(
    now: datetime.datetime,
    i: int,
    t_date: AnnualDate,
    t_time: Time = Time("00:00")
) -> datetime.datetime:
    """
    Schedule every year on {mm/dd} at {time}?

    Ex:
    every year on 1/1
    every year on 7/4 at 21:00
    """
    reference = now.replace(month=t_date.month, day=t_date.day, year=now.year)
    reference = reference.replace(hour=t_time.hour, minute=t_time.minute, second=t_time.second, microsecond=0, tzinfo=now.tzinfo)

    if now >= reference:
        next_instance = reference.replace(year=reference.year + (i+1))
    else:
        next_instance = reference.replace(year=reference.year + i)

    return next_instance


@timeline(f"on {DayOfMonth} of (each|the) month( at {Time})?")
def on_dayofmonth_of_each_month_at_time(
    now: datetime.datetime,
    i: int,
    t_day: DayOfMonth,
    t_time: Time = Time("00:00")
) -> datetime.datetime:
    """
    Schedule on {day_of_month} of each month at {time}?

    Ex:
    on day 7 of each month
    on day 15 of each month at 8:45
    """
    reference = now.replace(day=t_day.day)
    reference = reference.replace(hour=t_time.hour, minute=t_time.minute, second=t_time.second, microsecond=0, tzinfo=now.tzinfo)

    if now >= reference:
        m, y = month_step(i+1, reference.month, reference.year)
    else:
        m, y = month_step(i, reference.month, reference.year)

    return reference.replace(year=y, month=m)


@timeline(f"on the {Ordinal} day of (each|the) month( at {Time})?")
def on_the_ordinal_day_of_the_month_at_time(
    now: datetime.datetime,
    i: int,
    t_ordinal: Ordinal,
    t_time: Time = Time("00:00")
) -> datetime.datetime:
    """
    Schedule on the {ordinal} day of the month at {time}?

    Ex:
    on the 2nd day of the month at 00:00
    on the 1st day of each month
    """
    return on_dayofmonth_of_each_month_at_time(now, i, DayOfMonth(str(t_ordinal.number)), t_time)


@timeline(f"next {Season}")
def next_season(
    now: datetime.datetime,
    i: int,
    t_season: Season
) -> datetime.datetime:
    """
    Schedule next {season}

    Ex: "next spring", "next winter"

    Note that this returns astronomical seasons, I.E, equinoxes and solstices.
    As such, these do NOT begin at midnight on the day of, they begin whenever
    the solar event takes place. Further, aware datetimes are required for
    this, as the time it happens depends entirely on your timezone.
    """
    reference = get_solar_event_for_year(now.year, t_season.season)
    
    if reference <= now:
        next_instance = get_solar_event_for_year(now.year + (i+1), t_season.season)
    else:
        next_instance = get_solar_event_for_year(now.year + i, t_season.season)
    
    return next_instance.astimezone(now.tzinfo)


@timeline(f"next meteorological {Season}")
def next_meteorological_season(
    now: datetime.datetime,
    i: int,
    t_season: Season
) -> datetime.datetime:
    """
    Schedule next meteorological {season}

    Ex: "next meteorological spring", "next meteorological winter"

    As the string implies, this works with meteorological seasons, not
    astronomical events. Spring begins on March 1st at midnight, Summer on June
    1st, Autumn on September 1st, and so on.
    """
    reference = datetime.datetime(now.year, t_season.met_begin.month, t_season.met_begin.day, 0, 0, 0, tzinfo=now.tzinfo)

    if reference <= now:
        return datetime.datetime(now.year + (i+1), t_season.met_begin.month, t_season.met_begin.day, 0, 0, 0, tzinfo=now.tzinfo)
    else:
        return datetime.datetime(now.year + i, t_season.met_begin.month, t_season.met_begin.day, 0, 0, 0, tzinfo=now.tzinfo)
    

@timeline(f"on the {Ordinal} {Weekday} of the month( at {Time})?")
def on_the_ordinal_weekday_of_the_month_at_time(
    now: datetime.datetime,
    i: int,
    t_ordinal: Ordinal,
    t_weekday: Weekday,
    t_time: Time = Time("0:00")
) -> datetime.datetime:
    if t_ordinal.number > 5:
        raise ValueError(f"It is not possible for a month to have more than 5 occurrances of a day of the week. Thus, the '{t_ordinal.text} {t_weekday.text}' is invalid.")

    reference = ord_weekday_eval(now, 0, t_ordinal, t_weekday, t_time)

    if reference <= now:
        date = ord_weekday_eval(now, i+1, t_ordinal, t_weekday, t_time)
    else:
        date = ord_weekday_eval(now, i, t_ordinal, t_weekday, t_time)
    
    return date


@timeline(f"on the last {Weekday} of the month( at {Time})?")
def on_the_last_weekday_of_the_month_at_time(
    now: datetime.datetime,
    i: int,
    t_weekday: Weekday,
    t_time: Time = Time("0:00")
) -> datetime.datetime:
    reference = last_weekday_eval(now, 0, t_weekday, t_time)

    if reference <= now:
        return last_weekday_eval(now, i+1, t_weekday, t_time)
    else:
        return last_weekday_eval(now, i, t_weekday, t_time)
        

all_cyclical_timelines = [
    every_year_on_annualdate_at_time,
    every_timedelta_at_time,
    every_day_at_time,
    every_weekday_at_time,
    on_the_last_day_of_the_month_at_time,
    timedelta_before_the_last_day_of_the_month_at_time,
    on_dayofmonth_of_each_month_at_time,
    on_the_ordinal_day_of_the_month_at_time,
    next_season,
    next_meteorological_season,
    on_the_ordinal_weekday_of_the_month_at_time,
    on_the_last_weekday_of_the_month_at_time,

    # Some timelines need to occur later in the list.
    # This is because they can conflict with more specific
    # timelines.
    at_time,
]