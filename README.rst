tzcron
######

A library to work with cron/quartz expressions and timezones.

Overview
########

tzcron provides a way to define schedules attached to timezones and get time occurrences out of it by just iterating the object created.

Install
#######

>>> pip install tzcron

Usage
#####

>>> import tzcron
>>> import pytz
>>> schedule = tzcron.Schedule("* * * * * *", pytz.utc)
>>> str(schedule)
'Cron: * * * * * * @UTC [2016-09-25 19:10:48.948486+00:00->None]'
>>> next(schedule)
datetime.datetime(2016, 9, 25, 19, 11, tzinfo=<UTC>)
>>> next(schedule)
datetime.datetime(2016, 9, 25, 19, 12, tzinfo=<UTC>)
>>> next(schedule)
datetime.datetime(2016, 9, 25, 19, 13, tzinfo=<UTC>)


For further information, check the `official documentation <https://readthedocs.org/projects/tzcron/>`_


Develop this package
####################

To test the package::

 > python -m nose

To release a new version of the package::

 > python setup.py sdist bdist_wheel upload

