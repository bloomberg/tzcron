Filters
#######

The library has support for custom application filters, this allows you to pass multiple
filters to customize the schedule with some of your business logic.

You can pass those functions as a list on the filters argument of the schedule.

As an example, if we want to get occurrences that have the same hour and minute you
can use the following function:

>>> def is_funny_date(occurrence):
...     return occurrence.minute == occurrence.hour
...
>>> schedule = tzcron.Schedule("* * * * * *", pytz.utc, filters=[is_funny_date])
>>> [s.isoformat() for s in itertools.islice(schedule, 2)]
['2016-09-25T22:22:00+00:00', '2016-09-25T23:23:00+00:00']


The custom function interact with the library in three ways:

- Return True to mark the occurrence as valid
- Return True to mark skip the occurrence
- Raise StopIteration to halt the iterator


For an occurrence to be returned it should satisfy all filters.
