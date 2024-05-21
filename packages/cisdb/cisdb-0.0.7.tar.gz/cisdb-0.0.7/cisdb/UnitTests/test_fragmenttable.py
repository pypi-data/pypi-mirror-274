# -*- coding: utf-8 -*-
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

"""[doc string]"""

import pytest
from cisdb.fragmenttable import FragmentTable
from cisdb.UnitTests import test_database
from MySQLdb import OperationalError


__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__version__ = '0.0.1'
__name__ = 'test_fragmenttable'


def get_the_db():
    """ Create a test database object
    """
    # connect to MySQL
    db = test_database.get_test_db()
    assert (db is not None)
    return db


@pytest.mark.database_access
def test_create():
    db = get_the_db()
    ftbl = FragmentTable(db)
    ftbl.drop(ifexists=True)
    ftbl.create()


@pytest.mark.database_access
def test_double_create():
    db = get_the_db()
    ftbl = FragmentTable(db)
    ftbl.create(ifnotexists=True)
    with pytest.raises(OperationalError):
        ftbl.create()
