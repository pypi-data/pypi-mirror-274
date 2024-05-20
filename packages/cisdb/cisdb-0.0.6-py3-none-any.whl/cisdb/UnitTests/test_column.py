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

from basedb.column import Column

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__version__ = '0.0.1'
__name__ = 'test_-column'

# some column definition dictionaries for testing
c1parm = {'name': 'id', 'type': int, 'autoincrement': True, 'length': 4,
                  'primary': True, 'comment': 'internal id number'}
c2parm = {'name': 'name', 'type': str, 'length': 64, 'indexKey': True,
                  'comment': 'Channel name', 'unique': True}

# list of column definitions
test_cols = [c1parm, c2parm]


def test_columdef():
    for parm in test_cols:
        col = Column(**parm)
        coldef = col.get_column_def()
        assert (coldef is not None)
