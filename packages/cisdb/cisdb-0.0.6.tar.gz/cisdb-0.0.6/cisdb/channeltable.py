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

"""Class representing a channel in the CIS"""

from cisdb.channelrow import ChannelRow

from basedb.table import Table

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__name__ = 'ChannelTable'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'


class ChannelTable(Table):

    def __init__(self, db, name=None):
        self.row = ChannelRow()
        if not name:
            name = 'Channels'
        super().__init__(db, name, columns=self.row.get_col_def(),
                         comment='Known channels')
        self.row = ChannelRow()
