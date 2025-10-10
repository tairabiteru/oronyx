from collections.abc import Callable
import datetime
import re

from .determinants import all_timelines, all_pasts, all_futures
from .impl import Timeline, Past, Future
from .tokens import *


def get_blank_timeline(time_string: str) -> Timeline | None:
    for timeline in all_timelines:
        match = re.search(timeline.regex, time_string)

        if match: 
            return timeline
    else:
        return None


def get_timeline(now: datetime.datetime, time_string: str) -> Timeline:
    timeline = get_blank_timeline(time_string)

    if timeline is None:
        raise ValueError(f"String '{time_string}' did not match any schedulers.")
    
    timeline = timeline.set_now(now).set_logic(time_string)
    assert isinstance(timeline, Timeline)
    return timeline


def get_past_obj(time_string: str) -> Callable[[datetime.datetime, str], datetime.datetime] | None:
    for past in all_pasts:
        assert isinstance(past, Past)
        match = re.search(past.regex, time_string)
        
        if match:
            return past
    else:
        return None


def get_past(now: datetime.datetime, time_string: str) -> datetime.datetime:
    determinant = get_past_obj(time_string)
    if determinant is None:
        raise ValueError(f"No past determinant exists for the time string '{time_string}'")
    return determinant(now, time_string)


def get_future_obj(time_string: str) -> Callable[[datetime.datetime, str], datetime.datetime] | None:
    for future in all_futures:
        assert isinstance(future, Future)
        match = re.search(future.regex, time_string)
        
        if match:
            return future
    else:
        return None


def get_future(now: datetime.datetime, time_string: str) -> datetime.datetime:
    determinant = get_future_obj(time_string)
    if determinant is None:
        raise ValueError(f"No future determinant exists for the time string '{time_string}'")
    return determinant(now, time_string)


__all__ = (
    "get_blank_timeline",
    "get_timeline",
    "get_future_obj",
    "get_future",
    "get_past_obj",
    "get_past",
    "impl",
    "tokens"
)