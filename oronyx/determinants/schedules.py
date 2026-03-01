import datetime

from ..impl import schedule
from ..tokens import Time, TimeDelta, Weekday
from .periods import on_weekday_time_to_time


@schedule(f"(on )? weekdays? (from|between) {Time} ?(and|&|to|-) ? {Time}")
def on_weekdays_time_to_time(
    now: datetime.datetime,
    t_weekday: Weekday,
    t_start: Time,
    t_end: Time
) -> list[tuple[datetime.datetime, datetime.datetime]]:
    start, end = time_to_time(now, f"{t_start.text} to {t_end.text}")

    while start.weekday() != t_weekday.number:
        now += datetime.timedelta(days=1)
        start, end = time_to_time(now, f"{t_start.text} to {t_end.text}")
    
    if end < now:
        now += datetime.timedelta(days=1)
        return on_weekday_time_to_time(now, f"On {t_weekday.text} from {t_start.text} to {t_end.text}")
    
    return start, end


all_schedules = [
    on_weekdays_time_to_time
]