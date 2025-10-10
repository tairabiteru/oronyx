from __future__ import annotations
from collections.abc import Callable
import datetime
from typing import Concatenate

from .base import Determinant
from ..tokens import Token


class Past(Determinant):
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


def past(regex: str) -> Callable[[Callable[Concatenate[datetime.datetime, ...], datetime.datetime]], Past]:
    """
    Decorator which creates a "past determinant." A function which
    acts as a shortcut to using a timeline to determine a past
    time.
    
    regex: str
        The regex string which is used for the past.
    """
    def inner(past_determinant: Callable[Concatenate[datetime.datetime, ...], datetime.datetime]) -> Past:
        return Past(past_determinant, regex)
    return inner