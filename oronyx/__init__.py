import datetime
import re
import typing as t

from .schedulers import schedulers


def get_scheduler(cron_string: str) -> t.Callable:
    for scheduler in schedulers:
        match = re.search(scheduler.regex, cron_string)

        if match: 
            return scheduler
    else:
        return None


def get_future(now: datetime.datetime, cron_string: str) -> datetime.datetime:
    scheduler = get_scheduler(cron_string)

    if scheduler is not None:
        return scheduler(now, cron_string)
    else:
        raise ValueError(f"String '{cron_string}' did not match any schedulers.")
