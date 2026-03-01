from __future__ import annotations
from collections.abc import Callable
import datetime
from typing import Concatenate

from .base import Determinant
from ..tokens import Token


class Period(Determinant):
    def __init__(
            self,
            determinant: Callable[Concatenate[datetime.datetime, ...], tuple[datetime.datetime, datetime.datetime]], 
            regex: str
        ):
        self.determinant = determinant
        self.regex = regex

        self._time_string: str | None = None
        self._tokens: list[Token] | None = None
        self._now: datetime.datetime | None = None
    
    def __call__(self, now: datetime.datetime, time_string: str) -> tuple[datetime.datetime, datetime.datetime]:
        now = now.replace(microsecond=0)
        self.set_now(now).set_logic(time_string)
        return self.determinant(now, *self.tokens)


def period(regex: str) -> Callable[[Callable[Concatenate[datetime.datetime, ...], tuple[datetime.datetime, datetime.datetime]]], Period]:
    def inner(determinant) -> Period:
        return Period(determinant, regex)
    return inner