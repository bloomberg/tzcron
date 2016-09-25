Daylight Saving Times
#####################

You might be wondering how will this behave after a DST change in a timezone.

DST Changes
-----------

As an example, lets say we want to schedule for 8:30 at Madrid timezone, but they have
a DST change on the 30th of october, using the tzcron module will handle it as shown:

>>> import datetime as dt
>>> import pytz
>>> import tzcron
>>> madrid_tz = pytz.timezone("Europe/Madrid")
>>> start_t = madrid_tz.localize(dt.datetime(2016, 10, 29))
>>> schedule = tzcron.Schedule("30 8 * * * *", madrid_tz, start_t)
>>> [s.isoformat() for s in itertools.islice(schedule, 2)]
['2016-10-29T08:30:00+02:00', '2016-10-30T08:30:00+01:00']

Note the first occurrence is in +2 whilst the second is in +1

Schedules in the change
-----------------------

There is though a catch, what happens if you schedule something
at 2:30 (in the middle of the change). This is a tricky situation, and ideally
you should try to avoid it. if for whatever reason you have to deal with it,
this is how tzcron behaves:

When we move our clocks back (times happening twice):

>>> madrid_tz = pytz.timezone("Europe/Madrid")
>>> start_t = madrid_tz.localize(dt.datetime(2016, 10, 29))
>>> schedule = tzcron.Schedule("30 2 * * * *", madrid_tz, start_t)
>>> [s.isoformat() for s in itertools.islice(schedule, 2)]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 1, in <listcomp>
  File "tzcron.py", line 125, in __next__
    next_it = self.t_zone.localize(next_it, is_dst=None)
  File "pytz/tzinfo.py", line 349, in localize
    raise AmbiguousTimeError(dt)
pytz.exceptions.AmbiguousTimeError: 2016-10-30 02:30:00

When we move our clocks forward (times not happening):

>>> start_t = madrid_tz.localize(dt.datetime(2016, 3, 26))
>>> schedule = tzcron.Schedule("30 2 * * * *", madrid_tz, start_t)
>>> [s.isoformat() for s in itertools.islice(schedule, 2)]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 1, in <listcomp>
  File "tzcron.py", line 125, in __next__
    next_it = self.t_zone.localize(next_it, is_dst=None)
  File "pytz/tzinfo.py", line 327, in localize
    raise NonExistentTimeError(dt)
pytz.exceptions.NonExistentTimeError: 2016-03-27 02:30:00


Note this is done in purpose, handling those cases is part of your business logic
and there is no good way to do it in the library, you can just capture those exceptions
and handle those time. The schedule iterator is moved so the next time you call it
it will return the next occurrence.
