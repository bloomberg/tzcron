#!/usr/bin/env python

# Copyright 2015 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from setuptools import setup

setup(
    name='tzcron',
    version='1.0.0',
    description='Timezone aware Cron/Quartz parser',
    license="Apache",
    py_modules=['tzcron'],
    install_requires=['python-dateutil', 'six', 'pytz'],
    url='https://github.com/bloomberg/tzcron',
    author='Mario Corchero',
    author_email='mariocj89@gmail.com',
    test_suite='nose.collector',
    tests_require=['ddt'],
    keywords=[
        'cron',
        'time',
        'datetime',
        'timezone',
        'quartz',
        'schedule',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
