import datetime

from .decorators import scheduler
from .tokens import TimeDelta, Time, Weekday, AnnualDate, DayOfMonth
from .utils import get_last_day_of_month


@scheduler(f"every {TimeDelta}( at {Time})?")
def every_timedelta_at_time(
        now: datetime.datetime,
        t_delta: TimeDelta, 
        t_time: Time | None = Time("00:00")
    ) -> datetime.datetime:
    """
    Schedule every {timedelta} at {time}?

    Ex:
    every 2 days
    every 1 week at 13:00
    every 6 seconds
    """
    future = now + t_delta.delta
    future = future.replace(hour=t_time.hour, minute=t_time.minute, second=t_time.second, microsecond=0)
    return future


@scheduler(f"every ?day( at {Time})?")
def everyday_at_time(
    now: datetime.datetime,
    t_time: Time | None = None
) -> datetime.datetime:
    """
    Schedule every day at {time}?
    Shortcut to "every 1 days at {time}"

    Ex:
    everyday at 10:00
    every day at 12:30
    every day
    """
    return every_timedelta_at_time(now, f"every 1 days at {t_time.text}")


@scheduler(f"at {Time}")
def at_time(
    now: datetime.datetime,
    t_time: Time
) -> datetime.datetime:
    """
    Schedule at {time}
    Shortcut to every 1 days at {time}

    Ex:
    at 9:34
    """
    return every_timedelta_at_time(now, f"every 1 days at {t_time.text}")


@scheduler(f"every {Weekday}( at {Time})?")
def every_weekday_at_time(
        now: datetime.datetime,
        t_weekday: Weekday, 
        t_time: Time | None = Time("00:00")
    ) -> datetime.datetime:
    """
    Schedule every {weekday} at {time}?

    Ex:
    every tuesday at 8:30
    every friday
    """
    future = now.replace(hour=t_time.hour, minute=t_time.minute, second=t_time.second, microsecond=0)

    while future.weekday() != t_weekday.number:
        future += datetime.timedelta(days=1)

    if future < now:
        future += datetime.timedelta(days=7)
    return future


@scheduler(f"on {Weekday}( at {Time})?")
def on_weekday_at_time(
    now: datetime.datetime,
    t_weekday: Weekday,
    t_time: Time | None = Time("00:00")
) -> datetime.datetime:
    """
    Schedule on {weekday} at {time}?
    Shortcut to "every {weekday} at {time}

    Ex:
    on wednesdays
    on sundays at 13:45
    """
    return every_weekday_at_time(now, f"every {t_weekday.text} at {t_time.text}")


@scheduler(f"on the last day of the month( at {Time})?")
def on_the_last_day_of_the_month_at_time(
        now: datetime.datetime,
        t_time: Time | None = Time("00:00")
) -> datetime.datetime:
    """
    Schedule on the last day of the month at {time}?

    On leap years, this will return the 29th of February.

    Ex:
    on the last day of the month
    on the last day of the month at 23:59
    """
    last_day_this_month = get_last_day_of_month(now.month, now.year)
    last_day_this_month = datetime.datetime(now.year, now.month, last_day_this_month)
    target = last_day_this_month.replace(hour=t_time.hour, minute=t_time.minute, second=t_time.second)

    if target < now:
        if now.month == 12:
            month = 1
            year = now.year + 1
        else:
            month = now.month + 1
            year = now.year

        last_day_this_month = get_last_day_of_month(month, year)
        last_day_this_month = datetime.datetime(year, month, last_day_this_month)
        target = last_day_this_month.replace(hour=t_time.hour, minute=t_time.minute, second=t_time.second)
    
    return target


@scheduler(f"{TimeDelta} before the last day of the month( at {Time})?")
def timedelta_before_the_last_day_of_the_month_at_time(
    now: datetime.datetime,
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
    target = on_the_last_day_of_the_month_at_time(now, f"on the last day of the month at {t_time.text}")
    
    target -= t_delta.delta

    if target < now:
        current = now.month
        while now.month == current:
            now += datetime.timedelta(days=1)
        return timedelta_before_the_last_day_of_the_month_at_time(
            now, 
            f"{t_delta.text} before the last day of the month at {t_time.text}"
        )
            
    return target


@scheduler(f"every year on {AnnualDate}( at {Time})?")
def every_year_on_annualdate_at_time(
    now: datetime.datetime,
    t_date: AnnualDate,
    t_time: Time | None = Time("00:00")
) -> datetime.datetime:
    """
    Schedule every year on {mm/dd} at {time}?

    Ex:
    every year on 1/1
    every year on 7/4 at 21:00
    """
    future = now.replace(month=t_date.month, day=t_date.day)
    future = future.replace(hour=t_time.hour, minute=t_time.minute, second=t_time.second, microsecond=0)

    if future > now:
        return future
    
    while future < now or (future.day != t_date.day or future.month != t_date.month):
        future += datetime.timedelta(days=1)
    return future


@scheduler(f"on {DayOfMonth} of each month( at {Time})?")
def on_dayofmonth_of_each_month_at_time(
    now: datetime.datetime,
    t_day: DayOfMonth,
    t_time: Time | None = Time("00:00")
) -> datetime.datetime:
    """
    Schedule on {day_of_month} of each month at {time}?

    Ex:
    on day 7 of each month
    on day 15 of each month at 8:45
    """
    future = now.replace(day=t_day.day)
    future = future.replace(hour=t_time.hour, minute=t_time.minute, second=t_time.second, microsecond=0)

    if future > now:
        return future

    while future < now or future.day != t_day.day:
        future += datetime.timedelta(days=1)
    return future


schedulers = [
    every_timedelta_at_time,
    everyday_at_time,
    every_weekday_at_time,
    on_weekday_at_time,
    on_the_last_day_of_the_month_at_time,
    timedelta_before_the_last_day_of_the_month_at_time,
    every_year_on_annualdate_at_time,
    on_dayofmonth_of_each_month_at_time,

    # Less specific schedulers go last
    at_time
]