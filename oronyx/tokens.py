import datetime
import re

from typing import TypeVarTuple


Tokens = TypeVarTuple('Tokens')


class Meta(type):
    def __repr__(self):
        return self.regex # type: ignore


class Token(metaclass=Meta):
    """
    A generic Token object.

    In Oronyx, a token is an object created by the lexer created when it lexes
    the strings passed into scheduler functions. These tokens can be quite
    varied in their nature, but common amongst all of them is that they have
    some text passed in, and that text must match a regular expression.

    Tokens also have their metaclass overridden by the above defined
    metaclass because this allows them to be used as shorthands in f-strings
    to reference their regular expression. This creates some very nice syntax
    that makes it easy to understand what a given scheduler is designed to
    match.

    Attributes
    ----------
    text: str
        The text which matches the regex.
    regex: str
        A regex pattern which matches the token.
    """
    regex: str
    text: str


class AbsoluteDate(Token):
    """
    A fully resolved date, one for which a weekday can be named.
    MM/DD/YYYY
    
    Ex: 8/20/2025

    Attributes
    ----------
    month: int
        The month.
    day: int
        The day.
    year: int
        The year.
    regex: str
        The regex which matches an absolute date token.
    text: str
        The original text which matches the regex.
    """
    regex = r"\d{1,2}\/\d{1,2}\/\d{4}"

    def __init__(self, text: str):
        self.text = text

        m, d, y = tuple(text.split("/"))
        m, d, y = map(int, [m, d, y])
        self.date = datetime.date(y, m, d)
    
    @property
    def month(self) -> int:
        return self.date.month
    
    @property
    def day(self) -> int:
        return self.date.day
    
    @property
    def year(self) -> int:
        return self.date.year


class AnnualDate(Token):
    """
    An annually occuring date, one without a year.
    MM/DD

    Ex: 7/4

    Attributes
    ----------
    month: int
        The month.
    day: int
        The day.
    regex: str
        The regex which matches an annual date token.
    text: str
        The original text which matches the regex.
    """
    regex = r"\d{1,2}\/\d{1,2}"

    def __init__(self, text: str):
        self.text = text

        m, d = tuple(text.split("/"))
        m, d = tuple(map(int, [m, d]))
        y = datetime.datetime.now().year

        for i in range(0, 3):
            try:
                datetime.date(y + i, m, d)
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"Invalid annual date {m}/{d}")
        
        self.month = m
        self.day = d
    
    @property
    def month_name(self) -> str:
        names = [
            None, "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        return names[self.month]


class DayOfMonth(Token):
    """
    A day of the month. Syntactically a bit weird, but
    formatted as "day 5" or "day 12"

    Ex: "day 9" (of August, for example)
    
    Attributes
    ----------
    day: int
        The day of the month.
    regex: str
        The regex which matches a day of month token.
    text: str
        The original text which matches the regex.
    """
    regex = r"day \d{1,2}"
    symbol = "{day_of_month}"

    def __init__(self, text: str):
        self.text = text

        self.day = int(text.split(" ")[-1])


class Weekday(Token):
    """
    A day of the week, optionally ends with "s".

    Ex: "sunday"

    Attributes
    ----------
    weekday: str
        The name of the weekday.
    number: int
        The weekday number, as would be returned by datetime.weekday()
    regex: str
        The regex which matches a weekday token.
    text: str
        The original text which matches the regex.
    """
    regex = r"((sun|mon|tues|wednes|thurs|fri|satur)days?){1}"

    def __init__(self, text: str):
        self.text = text
        
        if not text.endswith("y"):
            self.weekday = text[:-1]
        else:
            self.weekday = text
    
    @property
    def number(self) -> int:
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        return days.index(self.weekday)


class Time(Token):
    """
    A specific time of day, seconds optional.
    HH:MM:SS, 24 hour format.

    Ex: 12:30 or 23:59:59

    Attributes
    ----------
    hour: int
        The hour of the time.
    minute: int
        The minute of the time.
    second: int
        The second of the time.
    time: datetime.time
        A datetime.time object matching the time.
    regex: str
        The regex which matches a time token.
    text: str
        The original text which matches the regex.
    """
    regex = r"([0-1]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?"

    def __init__(self, text: str):
        self.text = text

        try:
            h, m, s = tuple(text.split(":"))
        except ValueError:
            h, m = tuple(text.split(":"))
            s = "0"
        
        h, m, s = tuple(map(int, [h, m, s]))
        self.time = datetime.time(hour=h, minute=m, second=s, microsecond=0)
    
    @property
    def hour(self) -> int:
        return self.time.hour
    
    @property
    def minute(self) -> int:
        return self.time.minute

    @property
    def second(self) -> int:
        return self.time.second


class TimeDelta(Token):
    """
    An amount of time passed, a *difference* in time.
    A time delta.

    Typically a number followed by a unit of time, but it the
    unit cannot be months because they are a non-specific amount
    of time.

    Ex: 25 seconds, 1 day, 6 years, 2 weeks

    Attributes
    ----------
    delta: datetime.timedelta
        A timedelta matching the amount of time.
    regex: str
        The regex which matches a time delta token.
    text: str
        The original text which matches the regex.
    """
    regex = r"\d+ (seconds?|minutes?|hours?|days?|weeks?|years?){1}"

    def __init__(self, text):
        self.text = text

        number, unit = tuple(text.split(" "))
        number = float(number)

        if "year" in unit:
            seconds = number * (86400 * 365)
        elif "week" in unit:
            seconds = number * (86400 * 7)
        elif "day" in unit:
            seconds = number * 86400
        elif "hour" in unit:
            seconds = number * 3600
        elif "minute" in unit:
            seconds = number * 60
        else:
            seconds = number
        
        self.delta = datetime.timedelta(seconds=seconds)


class Ordinal(Token):
    """
    An ordinal number.

    Ex: 21st, 43rd, 92nd, 6th

    Attributes
    ----------
    number: int
        The integer matching the ordinal.
    regex: str
        The regex which matches a time token.
    text: str
        The original text which matches the regex.
    """
    regex = r"\d+(st|nd|rd|th)"

    def __init__(self, text):
        self.text = text
        self.number = int(re.sub("(st|nd|rd|th)", "", text))


class Season(Token):
    """
    A season of the year.

    Ex: summer, winter, autumn, fall, spring

    Attributes
    ----------
    season: str
        The season. "fall" is always resolved to "autumn."
    regex: str
        The regex which matches a season token.
    text: str
        The original text which matches the regex.
    """
    regex = r"((spring)|(summer)|(fall)|(autumn)|(winter))"

    def __init__(self, text):
        self.text = text
        
        if self.text == "fall":
            self.season = "autumn"
        else:
            self.season = text
    
    @property
    def met_begin(self) -> AnnualDate:
        """
        The annual date associated with the meteorological start of the season.
        """
        match self.season:
            case "spring":
                return AnnualDate("3/1")
            case "summer":
                return AnnualDate("6/1")
            case "autumn":
                return AnnualDate("9/1")
            case "winter":
                return AnnualDate("12/1")
            case _:
                raise ValueError("This should never happen.")


all_tokens = [
    AbsoluteDate,
    AnnualDate,
    Weekday,
    Time,
    TimeDelta,
    Season,

    # Less specific tokens go last
    DayOfMonth,
    Ordinal
]