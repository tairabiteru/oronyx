from collections.abc import Callable
import datetime
import re

from .tokens import all_tokens, Token


def lex(future_string: str, tokens: list[Token] | None = None) -> list[Token]:
    """
    Given a "future string", produce a list of token objects.

    Note that these do **NOT NECESSARILY** return in the order
    they appear.

    Parameters
    ----------
    future_string: str
        The "future string" to be lexed.
    tokens: list[Token] | None = None
        The list of tokens. Only used when being called recursively.
    
    Returns
    -------
    list[Token]
        A list of tokens found in the future string.
    """
    if tokens == None:
        tokens = []

    for token in all_tokens:
        match = re.search(token.regex, future_string)

        if match:
            token = token(match.group())
            future_string = future_string.replace(match.group(), "")
            tokens.append(token)
            return lex(future_string, tokens=tokens)
    else:
        return tokens


class Scheduler:
    """
    Defines a Scheduler object.

    A scheduler object is central to oronyx's inner workings. They are defined
    as functions which take a future string (that is, some string describing a
    point in the future) and a point in time, and then apply the logic of the
    future string to the point in time to get a *future*.

    As an example, take the future string:
    "every 3 days at 12:00"

    If the datetime passed is August 3rd, 2025 at 15:30, then the next "future"
    of that time would occur at August 6th, 2025 at 12:00. 

    Attributes
    ----------
    func: Callable[[datetime.datetime, tuple[Token, ...]], datetime.datetime]
        A function which evaluates the time string by taking the current time
        and the tokens contained in the time string as arguments, and returns
        a datetime which matches the function's rule.
    regex: str
        The regex which is used to match a future string.
    name: str
        The name of the function which evaluates the future string. This is
        mainly used internally in tests to make sure that get_scheduler()
        returns the correct scheduler for a given string.
    """
    def __init__(
            self,
            func: Callable[[datetime.datetime, Token], datetime.datetime],
            regex: str
        ):

        self.func = func
        self.regex = regex
    
    @property
    def name(self) -> str:
        return self.func.__name__

    def __call__(self, now: datetime.datetime, future_string: str) -> datetime.datetime:
        if not re.match(self.regex, future_string):
            raise ValueError(f"The string '{future_string}' did not match the pattern '{self.regex}'")

        tokens = lex(future_string)
        tokens = sorted(tokens, key=lambda x: self.regex.find(x.regex))
        return self.func(now, *tokens)


def scheduler(regex: str) -> Callable[[Callable[[datetime.datetime, Token], datetime.datetime]], Scheduler]:
    """
    Decorator which acts as a shortcut to making a Scheduler.

    regex: str
        The regex string which is used for func.
    """
    def inner(func) -> Scheduler:
        return Scheduler(func, regex)
    return inner


class DeltaDeterminer:
    """
    
    """
    def __init__(
            self,
            func: Callable[[datetime.datetime, Token], datetime.datetime],
            regex: str
        ):

        self.func = func
        self.regex = regex
    
    @property
    def name(self) -> str:
        return self.func.__name__

    def __call__(self, now: datetime.datetime, delta_string: str) -> datetime.datetime:
        if not re.match(self.regex, delta_string):
            raise ValueError(f"The string '{delta_string}' did not match the pattern '{self.regex}'")

        tokens = lex(delta_string)
        tokens = sorted(tokens, key=lambda x: self.regex.find(x.regex))
        return self.func(now, *tokens)


def delta_determiner(regex: str) -> Callable[[Callable[[datetime.datetime, Token], datetime.datetime]], DeltaDeterminer]:
    """
    Decorator which acts as a shortcut to making a Scheduler.

    regex: str
        The regex string which is used for func.
    """
    def inner(func) -> DeltaDeterminer:
        return DeltaDeterminer(func, regex)
    return inner
