.. tzcron documentation master file, created by
   sphinx-quickstart on Sun Sep 25 20:30:47 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to tzcron's documentation!
==================================

Welcome to the documentation of the tzcron library,
a library to work with cron/quartz expressions and timezones.

Overview
########

tzcron provides a way to define schedules attached to timezones and get time occurrences
out of it by just iterating the object created.

You can look at it as a cron parser that accepts complex expressions and timezones,
it won't schedule anything for you, but it will make it easy to do it.

Contents:

.. toctree::
   :maxdepth: 2

   basic-usage
   complex-expressions
   filters
   dst
   leap-second
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

