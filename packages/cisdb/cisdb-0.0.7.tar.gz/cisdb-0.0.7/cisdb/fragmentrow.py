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

"""A class representing a row in the fragment table.
Fragments are the parsed pieces of a channel name separated by a delimiter.
"""

from basedb.row import Row

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__myname__ = 'fragmentrow'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'


class FragmentRow(Row):

    def __init__(self):
        super().__init__()
        self.__name__ = 'Fragment'
        self.id = 0
        self.name = ''
        self.description = ''

    def get_col_def(self):
        id_def = {'name': 'id', 'type': int, 'autoincrement': True,
                  'length': 4,
                  'primary': True, 'comment': 'internal id number'}
        name_def = {'name': 'name', 'type': str, 'length': 64, 'indexKey':
                    True, 'comment': 'Fragment text', 'unique': True}

        column_definitions = [id_def, name_def]
        self.define_cols(column_definitions)
        self.set_eq_cols(['name'])
        return self.cols
