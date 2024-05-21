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

"""Class for Dewcriptions of channels and fragments"""

from basedb.table import Table
from cisdb.descriptionrow import Description

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__myname__ = 'descriptionstable'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'


class Descriptions(Table):
    """
    Class representing the descriptions entered by people.
    This allows the complete rebuilding of the automated information
    while preserving manual efforts.
    """
    def __init__(self, db, name=None):
        self.row = Description()
        if not name:
            name = 'Descriptions'
        super().__init__(db, name, columns=self.row.get_col_def(),
                         comment='Fragments are the parsed pieces of a '
                                 'channel name separated by a delimiter.')
        self.row = Description()

    def insert_update_desc(self, name, new_desc):
        """
        Check if this item has a description if so the new info is merged
        else a new entry is inserted.
        NB: this method is used to ADD new descriptions. To change an
        existing description, to fix a typo for example use update
        :param new_desc: str or list of strings
        :return: None
        """
        new_row = Description()
        new_row.get_col_def()
        new_row.data['name'] = name
        new_row.data['descriptions'] = new_desc

        old_desc_list = self.read(where='name=\'{}\''.format(name))

        if old_desc_list:
            # name column must be unique so list len == 1 or 0
            old_desc = Description()
            old_desc.set(old_desc_list[0])
            if old_desc.needs_update(new_row):
                old_desc.merge(new_row)
                self.update(old_desc, 'name')
        else:
            self.insert(new_row)
