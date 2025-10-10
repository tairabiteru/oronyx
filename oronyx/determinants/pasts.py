import datetime

from ..impl import past
from ..tokens import Time, TimeDelta, Weekday
from .timelines import every_timedelta_at_time, every_weekday_at_time


@past(f"{TimeDelta} (ago|before)( at {Time})?")
def timedelta_agobefore_at_time(
    now: datetime.datetime,
    t_delta: TimeDelta,
    t_time: Time = Time("0:00")
) -> datetime.datetime:
    return every_timedelta_at_time(now, -2, t_delta, t_time)


@past(f"on the {Weekday} before( at {Time})?")
def on_the_weekday_before_at_time(
    now: datetime.datetime,
    t_weekday: Weekday,
    t_time: Time = Time("0:00")
) -> datetime.datetime:
    return every_weekday_at_time(now, -2, t_weekday, t_time)


@past(f"last {Weekday}( at {Time})?")
def last_weekday_at_time(
    now: datetime.datetime,
    t_weekday: Weekday,
    t_time: Time = Time("0:00")
) -> datetime.datetime:
    return on_the_weekday_before_at_time(now, f"on the {t_weekday.text} before at {t_time.text}")


all_pasts = [
    timedelta_agobefore_at_time,
    on_the_weekday_before_at_time,
    last_weekday_at_time
]