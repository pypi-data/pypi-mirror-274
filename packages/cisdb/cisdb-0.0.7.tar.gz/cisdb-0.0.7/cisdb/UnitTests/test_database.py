#!/usr/bin/env python
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2020 Joseph Areeda <joseph.areeda@ligo.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Init tests for Database class"""

import pytest
from basedb.database import Database

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__version__ = '0.0.1'
__process_name__ = 'test_database'


def get_testing_config():
    config = {'host': 'localhost', 'user': 'cis-tst', 'password': 'trey88,lacer', 'database': 'cistest'}
    return config


def get_test_db():
    config = get_testing_config()
    db = Database(dsn=config)
    return db


@pytest.mark.database_access
def test_connect_by_dict():
    db = get_test_db()
    assert (db is not None)


@pytest.mark.database_access
def test_connect_by_arg():
    config = get_testing_config()
    db = Database(config['user'], config['password'], config['host'],
                  config['database'])
    assert (db is not None)
