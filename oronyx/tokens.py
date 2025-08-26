import datetime


class Meta(type):
    def __repr__(self):
        return self.regex


class Token(metaclass=Meta):
    regex: str
    symbol: str
    text: str


class AbsoluteDate(Token):
    regex = r"\d{1,2}\/\d{1,2}\/\d{4}"
    symbol = "{absolute_date}"

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
    regex = r"\d{1,2}\/\d{1,2}"
    symbol = "{annual_date}"

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
    regex = r"day \d{1,2}"
    symbol = "{day_of_month}"

    def __init__(self, text: str):
        self.text = text

        self.day = int(text.split(" ")[-1])


class Weekday(Token):
    regex = r"((sun|mon|tues|wednes|thurs|fri|satur)days?){1}"
    symbol = "{weekday}"

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
    regex = r"([0-1]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?"
    symbol = "{time}"

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
    regex = r"\d+ (seconds?|minutes?|hours?|days?|weeks?|years?){1}"
    symbol = "{delta}"

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


all_tokens = [
    AbsoluteDate,
    AnnualDate,
    Weekday,
    Time,
    TimeDelta,

    # Less specific tokens go last
    DayOfMonth
]