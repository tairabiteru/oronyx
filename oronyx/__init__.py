import datetime
import re

from .timeline import Timeline
from .determinants import all_timelines


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
    
    return timeline.set_now(now).set_logic(time_string)