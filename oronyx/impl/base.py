from __future__ import annotations
from collections.abc import Callable
import datetime
import re

from ..tokens import all_tokens, Token


def lex(time_string: str, tokens: list[Token] | None = None) -> list[Token]:
    """
    Given a "time string", produce a list of token objects.

    Note that these do **NOT NECESSARILY** return in the order
    they appear. We sort them later.

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


class Determinant:
    """
    A determinant base.
    """
    def __init__(
            self,
            determinant: Callable, 
            regex: str
        ):
        self.determinant = determinant
        self.regex = regex

        self._time_string: str | None = None
        self._tokens: list[Token] | None = None
        self._now: datetime.datetime | None = None
        
    
    @staticmethod
    def clean_time_string(time_string: str) -> str:
        return time_string.strip().lower()

    def set_now(self, now: datetime.datetime) -> Determinant:
        self._now = now
        return self
    
    def set_logic(self, time_string: str) -> Determinant:
        self._time_string = self.clean_time_string(time_string)
        self._tokens = None
        return self
    
    def matches(self, time_string: str) -> bool:
        time_string = self.clean_time_string(time_string)
        match = re.search(self.regex, time_string)
        
        if not match:
            return False
        
        time_string = time_string.replace(match.group(), "")
        if not time_string:
            return True
        
        return False
            
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
    def tokens(self) -> tuple[Token, ...]:
        if self._tokens is None:
            self._tokens = lex(self.time_string)
            self._tokens = sorted(self._tokens, key=lambda x: self.regex.find(x.regex))
        return tuple(self._tokens)