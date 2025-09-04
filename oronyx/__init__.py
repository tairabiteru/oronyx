import datetime
import re

from .schedulers import schedulers
from .deltas import delta_determiners
from .decorators import Scheduler, DeltaDeterminer


def get_scheduler(future_string: str) -> Scheduler | None:
    for scheduler in schedulers:
        match = re.search(scheduler.regex, future_string)

        if match: 
            return scheduler
    else:
        return None


def get_future(now: datetime.datetime, future_string: str) -> datetime.datetime:
    scheduler = get_scheduler(future_string)

    if scheduler is not None:
        return scheduler(now, future_string)
    else:
        raise ValueError(f"String '{future_string}' did not match any schedulers.")


def get_delta_determiner(delta_string: str) -> DeltaDeterminer | None:
    for delta_determiner in delta_determiners:
        match = re.search(delta_determiner.regex, delta_string)

        if match:
            return delta_determiner
    
    else:
        return None


def get_delta(now: datetime.datetime, delta_string: str) -> datetime.datetime:
    determiner = get_delta_determiner(delta_string)

    if determiner is not None:
        return determiner(now, delta_string)
    else:
        raise ValueError(f"String '{delta_string}' did not match any delta determiner.")