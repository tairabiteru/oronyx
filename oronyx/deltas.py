import datetime

from .decorators import delta_determiner
from .tokens import TimeDelta


@delta_determiner(f"{TimeDelta} before")
def timedelta_before(now: datetime.datetime, t_delta: TimeDelta) -> datetime.timedelta:
    return now - t_delta.delta


@delta_determiner(f"{TimeDelta} after")
def timedelta_after(now: datetime.datetime, t_delta: TimeDelta) -> datetime.timedelta:
    return now + t_delta.delta


delta_determiners = [
    timedelta_before,
    timedelta_after
]