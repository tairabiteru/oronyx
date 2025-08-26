import datetime
import re
import typing as t

from .tokens import all_tokens, Token


def lex(cron_string: str, tokens: list[Token] | None = None) -> list[Token]:
    if tokens == None:
        tokens = []

    for token in all_tokens:
        match = re.search(token.regex, cron_string)

        if match:
            token = token(match.group())
            cron_string = cron_string.replace(match.group(), "")
            tokens.append(token)
            return lex(cron_string, tokens=tokens)
    else:
        return tokens


def scheduler(regex: str):
    def inner(func):
        def wrapper(now: datetime.datetime, cron_string: str):
            tokens = lex(cron_string)
            tokens = sorted(tokens, key=lambda x: regex.find(x.regex))
            return func(now, *tokens)
        wrapper.regex = regex
        wrapper.name = func.__name__
        return wrapper
    inner.regex = regex
    return inner