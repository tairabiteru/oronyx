from __future__ import annotations
from collections.abc import Callable
import datetime
from typing import Concatenate

from .base import Determinant
from ..tokens import Token


class Future(Determinant):
    def __init__(
        self,
        determinant: Callable[Concatenate[datetime.datetime, ...], datetime.datetime],
        regex: str
    ):
        self.determinant = determinant
        self.regex = regex
        
        self._time_string: str | None = None
        self._tokens: list[Token] | None = None
        self._now: datetime.datetime | None = None

    def __call__(self, now: datetime.datetime, time_string: str) -> datetime.datetime:
        self.set_now(now).set_logic(time_string)
        return self.determinant(self.now, *self.tokens)


def future(regex: str) -> Callable[[Callable[Concatenate[datetime.datetime, ...], datetime.datetime]], Future]:
    """
    Decorator which creates a "future determinant." A function which
    acts as a shortcut to using a timeline to determine a future
    time.
    
    regex: str
        The regex string which is used for the past.
    """
    def inner(future_determinant: Callable[..., datetime.datetime]) -> Future:
        return Future(future_determinant, regex)
    return inner