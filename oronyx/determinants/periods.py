import datetime

from ..impl import period
from ..tokens import Time, TimeDelta, Weekday
from .timelines import at_time, every_weekday_at_time


@period(f"(everyday )?(from |between )?{Time} ?(and|&|to|-) ? {Time}")
def time_to_time(
    now: datetime.datetime,
    t_start: Time,
    t_end: Time
) -> tuple[datetime.datetime, datetime.datetime]:
    start = at_time(now, 0, t_start)
    end = at_time(now, 0, t_end)
    
    if start > now:
        start = at_time(now, -1, t_start)
    return start, end


@period(f"(on )?{Weekday} (from|between) {Time} ?(and|&|to|-) ? {Time}")
def on_weekday_time_to_time(
    now: datetime.datetime,
    t_weekday: Weekday,
    t_start: Time,
    t_end: Time
) -> tuple[datetime.datetime, datetime.datetime]:
    start, end = time_to_time(now, f"{t_start.text} to {t_end.text}")

    while start.weekday() != t_weekday.number:
        now += datetime.timedelta(days=1)
        start, end = time_to_time(now, f"{t_start.text} to {t_end.text}")
    
    if end < now:
        now += datetime.timedelta(days=1)
        return on_weekday_time_to_time(now, f"On {t_weekday.text} from {t_start.text} to {t_end.text}")
    
    return start, end


all_periods = [
    time_to_time,
    on_weekday_time_to_time
]