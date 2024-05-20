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

"""Exercise channel table"""

import pytest
from cisdb.channeltable import ChannelTable
from cisdb.channelrow import ChannelRow
from cisdb.UnitTests import test_database
from MySQLdb import OperationalError


__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__version__ = '0.0.1'
__name__ = 'test_channeltable'

tstname = 'ChannelTest'


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
    ctbl = ChannelTable(db, name=tstname)
    ctbl.drop(ifexists=True)
    ctbl.create()


@pytest.mark.database_access
def test_double_create():
    db = get_the_db()
    ctbl = ChannelTable(db, name=tstname)
    ctbl.create(ifnotexists=True)
    with pytest.raises(OperationalError):
        ctbl.create()


tst_rows = [
    {'name': 'chan-1', 'chan_types': 'type1',
     'data_types': ['dtype1', 'dtype2']},
    {'name': 'chan-2', 'chan_types': 'type2',
     'data_types': ['dtype3', 'dtype4']}
]


@pytest.mark.database_access
def test_add():
    db = get_the_db()
    ctbl = ChannelTable(db, name=tstname)
    ctbl.drop(ifexists=True)
    ctbl.create()
    ins_rows = list()
    for vals in tst_rows:
        r = ChannelRow().set(vals)
        ins_rows.append(r)

    ctbl.insert(ins_rows)
    cnt = ctbl.get_count()
    assert (cnt == len(tst_rows))

    rows = ctbl.read()
    assert (len(rows) == len(tst_rows))

    for idx in range(0, len(rows)):
        r = rows[idx]
        mydata = tst_rows[idx]
        for col in mydata.keys():
            if isinstance(r[col], list) and not isinstance(mydata[col], list):
                assert (r[col] == [mydata[col]])
            else:
                assert (r[col] == mydata[col])
