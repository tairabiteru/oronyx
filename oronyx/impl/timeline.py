from __future__ import annotations
from collections.abc import Callable
import datetime
from typing import Concatenate

from .base import Determinant
from ..tokens import Token


class Timeline(Determinant):
    """
    A timeline object.

    Central to Oronyx is the idea of a timeline. At its core, Oronyx is
    designed to produce these objects, which act like lists extending
    infinitely (mostly) into the future and the past. Timeline objects
    use a special function called a "determinant" which takes a current
    time, an index, and a set of Token objects as arguments, and which
    returns a datetime matching the index passed.

    Critically, a timeline will NEVER contain a "now". timeline[0] is
    the next occurrance, timeline[1], the occurance after that.
    timeline[-1] is the previous occurance to the now. The only time
    this is violated is if the matching time *IS* now, and even then,
    Oronyx considers this to be a past time.

    As an example, suppose the following time:
    September 9th, 2025 10:00

    Given the time string "every 2 days at 12:00" Oronyx will create
    a timeline object which does as follows:

    timeline[-2] == September 5th, 2025 12:00
    timeline[-1] == September 7th, 2025 12:00
    timeline[0] == September 9th, 2025 12:00
    timeline[1] == September 11th, 2025 12:00
    timeline[2] == September 13th, 2025 12:00
    """
    def __init__(
            self,
            determinant: Callable[Concatenate[datetime.datetime, int, ...], datetime.datetime], 
            regex: str
        ):
        self.determinant = determinant
        self.regex = regex

        self._time_string: str | None = None
        self._tokens: list[Token] | None = None
        self._now: datetime.datetime | None = None
    
    def __getitem__(self, i: int) -> datetime.datetime:
        return self.determinant(self.now, i, *self.tokens)
    
    def __call__(self, now: datetime.datetime, i: int, *tokens: ...) -> datetime.datetime:
        return self.determinant(now, i, *tokens)


def timeline(regex: str) -> Callable[[Callable[Concatenate[datetime.datetime, int, ...], datetime.datetime]], Timeline]:
    """
    Decorator which acts as a shortcut to make a Timeline
    from a determinant function.

    regex: str
        The regex string which is used for the timeline.
    """
    def inner(determinant) -> Timeline:
        return Timeline(determinant, regex)
    return inner