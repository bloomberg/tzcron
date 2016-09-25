Basic Usage
###########

In tzcron you can create a schedule through a cron expresion and a timezone.

Creating a Schedule
-------------------

>>> import tzcron
>>> import pytz
>>> schedule = tzcron.Schedule("* * * * * *", pytz.utc)
>>> str(schedule)
'Cron: * * * * * * @UTC [2016-09-25 19:10:48.948486+00:00->None]'

Iterating over the schedule
---------------------------

This object can be iterated to get all the occurrences of the specified schedule:

>>> next(schedule)
datetime.datetime(2016, 9, 25, 19, 11, tzinfo=<UTC>)
>>> next(schedule)
datetime.datetime(2016, 9, 25, 19, 12, tzinfo=<UTC>)
>>> next(schedule)
datetime.datetime(2016, 9, 25, 19, 13, tzinfo=<UTC>)

Limiting by start and end times
-------------------------------

You can also pass an start and end time, lets see an example to generate
all occurrences with minute=30 between now and two hours from now.

>>> import datetime as dt
>>> import tzcron
>>> import pytz
>>> now = dt.datetime.now(pytz.utc)  # '2016-09-25T20:10:20.916687+00:00'
>>> now_p2h = now + dt.timedelta(hours=2)
>>> schedule = tzcron.Schedule("30 * * * * *", pytz.utc, now, now_p2h)
>>> [s.isoformat() for s in schedule]
['2016-09-25T20:30:00+00:00', '2016-09-25T21:30:00+00:00']

When you not pass start it will be defaulted to now and end will be defaulted to never.

Using cron expressions
----------------------

Note that the first format is a cron expression (with year) that follows the pattern:

::

     * * * * * *
     | | | | | |
     | | | | | .. year (yyyy or * for any)
     | | | | ...... day of week (1 - 7) (1 to 7 are Monday to Sunday)
     | | | ........... month (1 - 12)
     | | ................ day of month (1 - 31)
     | ..................... hour (0 - 23)
     .......................... min (0 - 59)

To generate an occurrence every first day of a month at 10:30am:

>>> schedule = tzcron.Schedule("30 10 1 * * *", pytz.utc)
>>> [s.isoformat() for s in itertools.islice(schedule, 2)]
['2016-10-01T10:30:00+00:00', '2016-11-01T10:30:00+00:00']

Using timezones
---------------

Callers of the library can choose what timezone to generate the occurrences in.

For example, to generate occurrences every day at market open(8:30) in New York a client can use:

>>> schedule = tzcron.Schedule("30 10 1 * * *", pytz.timezone("America/New_York"))
>>> [s.isoformat() for s in itertools.islice(schedule, 2)]
['2016-10-01T10:30:00-04:00', '2016-11-01T10:30:00-04:00']

Note that the timezone of the schedules doesn't need to match with the timezone you pass
as start and end to limit the range of occurrences. In other words, you can ask the library
to give you all occurrences of 6:30 in London starting at 2016-06-01T00:00:00 in Sydney.

Tip: To see the list of available timezones on pytz:

>>> pytz.all_timezones
