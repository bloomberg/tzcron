"""
File that contains helper functions to get occurrences out of a cron expression
"""
import pytz
import re
import itertools
import datetime as dt
from dateutil import rrule

__all__ = ["TzCronizer"]

 # * * * * * *
 # | | | | | |
 # | | | | | .. year (yyyy or * for any)
 # | | | | ...... day of week (0 - 6) (0 to 6 are Monday to Sunday)
 # | | | ........... month (1 - 12)
 # | | ................ day of month (1 - 31)
 # | ..................... hour (0 - 23)
 # .......................... min (0 - 59)

class Parser(object):
    """Abstract class to create parsers for parts of quartz expressions

    Each parser can be user per token and a specific parser needs to provides
    the valid ranges of the quartz part and a dict of REPLACEMENTS in upper case

    See the specific parsers below (Ex: MinuteParser, WeekDayParser, etc..)

    All values:
        A star can be used to specify all valid values

    Multiple options:
        Each of the expression parsed can contain a list of expressions as a comma separated
        list. duplicates are removed
        Example: 0,1,4 Means 0, 1 and 4

    Ranges:
        A dash can be used to represent ranges
        2-5 Means 2 to 3

    Step:
        A slash can be used to specify a step
        Example: */2 Means to pick one of every two values.
                 if the valid range is 0 to 3 it will return 0 and 2

    Replacements:
        Each specific parser can define String replacements for the expression.
        Ex: JAN is ok for 1 (Jan) [ Case insensitive ]

    Other examples:
        "1,3-6,8" -> [1, 3, 4, 5, 6, 8].
        '1-3, 0-10/2" -> [0, 1, 2, 3, 4, 6, 8, 10]
    """

    MIN_VALUE = None  # Min value the expression can have
    MAX_VALUE = None  # Max value inclusive the expression can have
    REPLACEMENTS = {}  # String replacements for the expression.

    QUARTZ_REGEXP = re.compile(r"(?P<start>(\d+)|\*)(-(?P<end>\d+))?(/(?P<step>\d+))?")

    @classmethod
    def _parse_item(cls, expression):
        """Parses one of the comma separated expressions within the full quartz"""
        for key, value in cls.REPLACEMENTS.items():
            if key in expression.upper():
                expression = expression.upper().replace(key, value)
        matches = cls.QUARTZ_REGEXP.match(expression)
        assert matches, "Invalid expression: {}".format(expression)
        start = matches.group("start")
        end = matches.group("end") or start
        step = matches.group("step") or 1

        if start == "*":
            start = cls.MIN_VALUE
            end = cls.MAX_VALUE

        start = int(start)
        end = int(end)
        step = int(step)
        values = xrange(start, end + 1, step)

        if not all(cls.MIN_VALUE <= x <= cls.MAX_VALUE for x in values):
            raise ValueError("{} produces items out of {}".format(expression, cls.__name__))

        return values

    @classmethod
    def parse(cls, expression):
        """Parses the quartz expression

        :param expression: expression string encoded to parse
        returns: sorted list of unique elements resulting from the expression
        """
        groups = [cls._parse_item(item) for item in expression.split(',')]
        return sorted(list(set(itertools.chain(*groups))))


class MinuteParser(Parser):
    MIN_VALUE = 0
    MAX_VALUE = 59

class HourParser(Parser):
    MIN_VALUE = 0
    MAX_VALUE = 23

class MonthDayParser(Parser):
    MIN_VALUE = 1
    MAX_VALUE = 31

class MonthParser(Parser):
    MIN_VALUE = 1
    MAX_VALUE = 12
    REPLACEMENTS = {
        "JAN": "1",
        "FEB": "2",
        "MAR": "3",
        "APR": "4",
        "MAY": "5",
        "JUN": "6",
        "JUL": "7",
        "AUG": "8",
        "SEP": "9",
        "OCT": "10",
        "NOV": "11",
        "DEC": "12"
    }

class WeekDayParser(Parser):
    MIN_VALUE = 0
    MAX_VALUE = 6
    REPLACEMENTS = {
        "MON": "0",
        "TUE": "1",
        "WED": "2",
        "THU": "3",
        "FRI": "4",
        "SAT": "5",
        "SUN": "6"
    }


def parse_cron(expression):
    """parses a cron expression into a dict"""
    try:
        minute, hour, monthday, month, weekday, _ = expression.split(' ')
    except ValueError:
        raise ValueError("Invalid number of item in expression: {}".format(expression))

    result = {}
    result["bysecond"] = [0]
    if minute != "*":
        result["byminute"] = MinuteParser.parse(minute)
    if hour != "*":
        result["byhour"] = HourParser.parse(hour)
    if monthday != "*":
        result["bymonthday"] = MonthDayParser.parse(monthday)
    if month != "*":
        result["bymonth"] = MonthParser.parse(month)
    if weekday != "*":
        result["byweekday"] = WeekDayParser.parse(weekday)

    return result

def process(expresion, start_date, end_date=None):
    """
    Given a cron expresion and a start/end date returns an rrule
    Works with "naive" datetimes.
    """
    if start_date.tzinfo or (end_date and end_date.tzinfo):
        raise ValueError("Timezones are forbidden in this land.")

    arguments = parse_cron(expresion)

    # as rrule will strip out miliseconds, we need to do this hack :)
    # we could use .after but that changes the iface
    if start_date.second == 0 and start_date.microsecond != 0:
        start_date = start_date + dt.timedelta(0, 1)

    arguments["dtstart"] = start_date
    if end_date:
        arguments["until"] = end_date

    return rrule.rrule(rrule.MINUTELY, **arguments)



def get_year_filter(year):
    def year_filter(occurrence):
        if year == "*":
            return True
        else:
            valid_year = int(year)
            if occurrence.year < valid_year:
                return False
            elif occurrence.year > valid_year:
                raise StopIteration("Valid time already past")
            else:
                return True
    return year_filter


class TzCronizer(object):
    """Tz Cronizer allows to get a list of occurrences given an schedule and tz

    TzCronizer is a class that relying in dateutil.rrule generates a list of
    occurrences given an schedule, timezone and start-end date

    Once the TzCronizer is built, it is iterable. Being each element an
    occurrence of the schedule

    The cronizer provides no support for DST change times. It will throw an
    exception is a schedule falls into a DST change period.

    Filters allow to specify a filtering condition for the occurrence
    See year filter for an example
    """

    def __init__(self, expression, t_zone, start_date=None, end_date=None, filters=None):
        self.t_zone = t_zone
        self.expression = expression
        self.start_date = start_date or dt.datetime.now(pytz.utc)
        self.end_date = end_date

        if start_date.tzinfo is None or (end_date and end_date.tzinfo is None):
            raise ValueError("Start and Enddate should have a timezone")

        start_t = start_date.astimezone(self.t_zone)
        end_t = end_date.astimezone(self.t_zone) if end_date else None

        # all datetimes are in the desired tz. Lets strip out the timezones
        start_t = start_t.replace(tzinfo=None)
        end_t = end_t.replace(tzinfo=None) if end_t else None

        self.rrule = process(expression, start_t, end_t)
        self.rrule_iterator = iter(self.rrule)
        self.iter_num = 0
        self.filters = filters or []
        self.filters.append(get_year_filter(self.expression.split(" ")[-1]))

    def __str__(self):
        return "Cron: {} @{} [{}->{}]".format(self.expression, self.t_zone,
                                              self.start_date, self.end_date)

    def __iter__(self):
        return self

    def next(self):
        """
        Returns the next occurrence or raises StopIteration
        This method adds some extra validation for the returned
          iteration that are not natively handled by rrule
        """
        while True:
            next_it = next(self.rrule_iterator)
            next_it = self.t_zone.localize(next_it, is_dst=None)

            if not all([filt(next_it) for filt in self.filters]):
                continue

            return next_it
