Leap Second
###########

If you are here is because you are worried about how the library will behave with
leap seconds, good news is that the library has nothing to do with it. It just
returns occurrences of an expression. Also the minimal granularity is minutes,
all occurrences have second==0.

How you process them is up to your application but note that the python datetime
module has no support for leap second, so look for libraries like astropy to handle those.

This library can still be used in those situations though.