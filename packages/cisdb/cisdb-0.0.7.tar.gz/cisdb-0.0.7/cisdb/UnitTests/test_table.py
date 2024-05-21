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

"""Tests for the Table base class"""

import pytest

from basedb.table import Table
from basedb.column import Column
from cisdb.UnitTests import test_database, test_column

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__version__ = '0.0.1'
__name__ = 'test_table'


@pytest.mark.database_access
def get_the_db():
    # Create a test database
    db = test_database.get_test_db()
    assert (db is not None)
    return db


def get_column_definition():
    cols = list()
    col_names = list()
    for parm in test_column.test_cols:
        col_names.append(parm['name'])
        col = Column(**parm)
        coldef = col.get_column_def()
        assert (coldef is not None)
        cols.append(col)
    return cols


def test_create_table():
    db = get_the_db()
    cols = get_column_definition()
    tname = 'tst_tbl'
    table = Table(db, tname, columns=cols,
                  comment='just for fun')
    table.drop(ifexists=True)
    table.create()
    tblist = db.get_table_list()

    assert (len(tblist) == 1)
    assert (tname in tblist)

    col_list = table.get_column_list()
    assert (len(col_list) == len(cols))
    for col_dict in col_list:
        assert (next((c for c in cols if c.name == col_dict['Field']), None))
