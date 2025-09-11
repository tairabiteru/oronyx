from __future__ import annotations
from collections.abc import Callable
import datetime
import re

from .tokens import Token, all_tokens, Tokens


def lex(time_string: str, tokens: list[Token] | None = None) -> list[Token]:
    """
    Given a "time string", produce a list of token objects.

    Note that these do **NOT NECESSARILY** return in the order
    they appear.

    Parameters
    ----------
    time_string: str
        The "time string" to be lexed.
    tokens: list[Token] | None = None
        The list of tokens. Only used when being called recursively.
    
    Returns
    -------
    list[Token]
        A list of tokens found in the time string.
    """
    if tokens == None:
        tokens = []

    for token in all_tokens:
        match = re.search(token.regex, time_string)

        if match:
            token = token(match.group())
            time_string = time_string.replace(match.group(), "")
            tokens.append(token)
            return lex(time_string, tokens=tokens)
    else:
        return tokens


class Timeline:
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
            determinant: Callable[[datetime.datetime, int, *Tokens], datetime.datetime], 
            regex: str
        ):
        self.determinant = determinant
        self.regex = regex

        self._time_string: str | None = None
        self._tokens: list[Token] | None = None
        self._now: datetime.datetime | None = None

    def set_now(self, now: datetime.datetime) -> Timeline:
        self._now = now
        return self
    
    def set_logic(self, time_string: str) -> Timeline:
        self._time_string = time_string
        self._tokens = None
        return self
    
    @property
    def name(self) -> str:
        return self.determinant.__name__
    
    @property
    def time_string(self) -> str:
        if self._time_string is None:
            raise RuntimeError("No time string has been set.")
        return self._time_string
    
    @property
    def now(self) -> datetime.datetime:
        if self._now is None:
            raise RuntimeError("No now has been set.")
        return self._now
    
    @property
    def tokens(self) -> list[Token]:
        if self._tokens is None:
            self._tokens = lex(self.time_string)
            self._tokens = sorted(self._tokens, key=lambda x: self.regex.find(x.regex))
        return self._tokens
    
    def __getitem__(self, i: int) -> datetime.datetime:
        return self.determinant(self.now, i, *self.tokens)
    
    def __call__(self, now: datetime.datetime, i: int, *tokens: *Tokens) -> datetime.datetime:
        return self.determinant(now, i, *tokens)
    

def determinant(regex: str) -> Callable[[Callable[[datetime.datetime, int, *Tokens], datetime.datetime]], Timeline]:
    """
    Decorator which acts as a shortcut to make a Timeline
    from a determinant function.

    regex: str
        The regex string which is used for func.
    """
    def inner(determinant) -> Timeline:
        return Timeline(determinant, regex)
    return inner