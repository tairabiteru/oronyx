import datetime

from ..tokens import TimeDelta, Time, Weekday, AnnualDate
from ..impl import future
from .timelines import every_timedelta_at_time, every_weekday_at_time, every_year_on_annualdate_at_time


@future(f"in {TimeDelta}( at {Time})?")
def in_timedelta_at_time(
    now: datetime.datetime,
    t_delta: TimeDelta
) -> datetime.datetime:
    dt = every_timedelta_at_time(now, 0, t_delta)
    
    if (dt - now).total_seconds() < t_delta.delta.total_seconds():
        return every_timedelta_at_time(now, 1, t_delta)
    return dt


@future(f"{TimeDelta} from now( at {Time})?")
def timedelta_from_now_at_time(
    now: datetime.datetime,
    t_delta: TimeDelta,
    t_time: Time | None = None
) -> datetime.datetime:
    
    if t_time is None:
        return in_timedelta_at_time(now, f"in {t_delta.text}")
    
    return in_timedelta_at_time(now, f"in {t_delta.text} at {t_time.text}")


@future(f"at {Time}")
def at_time(
    now: datetime.datetime,
    t_time: Time
) -> datetime.datetime:
    t_delta = TimeDelta("1 day")
    return every_timedelta_at_time(now, 0, *[t_delta, t_time])


@future(f"next {Weekday}( at {Time})?")
def next_weekday_at_time(
    now: datetime.datetime,
    t_weekday: Weekday,
    t_time: Time = Time("0:00")
) -> datetime.datetime:
    return every_weekday_at_time(now, 0, *[t_weekday, t_time])


@future(f"on {AnnualDate}( at {Time})?")
def on_annualdate_at_time(
    now: datetime.datetime,
    t_date: AnnualDate,
    t_time: Time = Time("0:00")
) -> datetime.datetime:
    return every_year_on_annualdate_at_time(now, 0, *[t_date, t_time])


all_futures = [
    on_annualdate_at_time,
    in_timedelta_at_time,
    timedelta_from_now_at_time,
    next_weekday_at_time,
    at_time
]