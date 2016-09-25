Complex Expressions
###################

tzcron support cron expresions, you can familiarize with them `here <http://www.cronmaker.com/>`_.

But that is not all, it also supports most of the quartz format, you can find below
an example of the expressions that it accepts.

Replacements
------------

Weekdays and months can be passed as their english string representatiosn (3 letters).

If we want to get every thursday we can do:

>>> schedule = tzcron.Schedule("30 10 * * thu *", pytz.utc)
>>> [s.isoformat() for s in itertools.islice(schedule, 2)]
['2016-09-29T10:30:00+00:00', '2016-10-06T10:30:00+00:00']

To get days in january:

>>> schedule = tzcron.Schedule("30 10 * JAN * *", pytz.utc)
>>> [s.isoformat() for s in itertools.islice(schedule, 2)]
['2017-01-01T10:30:00+00:00', '2017-01-02T10:30:00+00:00']

Note it is case insensitive.

Multiple values
---------------

You can also provide multiple values on an option:

This returns mondays and tuesdays

>>> schedule = tzcron.Schedule("30 10 * * mon,tue *", pytz.utc)
>>> [s.isoformat() for s in itertools.islice(schedule, 3)]
['2016-09-26T10:30:00+00:00', '2016-09-27T10:30:00+00:00', '2016-10-03T10:30:00+00:00']


Ranges
------

Ranges can be specified with the '-', both values are inclusive.

>>> schedule = tzcron.Schedule("10-15 * * * * *", pytz.utc)
>>> [s.isoformat() for s in itertools.islice(schedule, 2)]
['2016-09-25T22:10:00+00:00', '2016-09-25T22:11:00+00:00']

Steps
-----

You can also ask for every X element

For example, passing a step of 20 to the minutes will give:

>>> schedule = tzcron.Schedule("*/20 * * * * *", pytz.utc)
>>> [s.isoformat() for s in itertools.islice(schedule, 2)]
['2016-09-25T22:00:00+00:00', '2016-09-25T22:20:00+00:00']


Combining Specs
---------------

All of the previous features can be combined at will, until your
mind blows up and you stop understanding your schedule.

As an example, to get tick on minutes between 0 and 10 that are pairs:

>>> schedule = tzcron.Schedule("0-10/2 * * * * *", pytz.utc)
>>> [s.isoformat() for s in itertools.islice(schedule, 4)]
['2016-09-25T22:00:00+00:00', '2016-09-25T22:02:00+00:00', '2016-09-25T22:04:00+00:00', '2016-09-25T22:06:00+00:00']


