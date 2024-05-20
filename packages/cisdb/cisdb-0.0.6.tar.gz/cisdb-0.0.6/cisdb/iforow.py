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

"""Class representing a row in the ifo table.
See Frame specification section 4.3.2.5 Detector Data -- FrDetector"""

from basedb.row import Row

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__myname__ = 'iforow'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'


class IfoRow(Row):

    def __init__(self):
        super().__init__()
        self.__name__ = 'IFO'
        self.id = 0
        self.name = ''
        self.description = ''

    def get_col_def(self):
        id_def = {'name': 'id', 'type': int, 'autoincrement': True,
                  'length': 4,
                  'primary': True, 'comment': 'internal id number'}
        name_def = {'name': 'name', 'type': str, 'length': 64, 'indexKey':
                    True, 'comment': 'Interferometer prefix', 'unique': True}
        dect_def = {'name': 'detector', 'type': str, 'length': 64,
                    'indexKey': True, 'comment': 'IFO name',
                    'unique': False}
        lat_def = {'name': 'latitude', 'type': float, 'length': 8,
                   'indexKey': False, 'comment': 'in radians',
                   'unique': False}
        lon_def = {'name': 'longitude', 'type': float, 'length': 8,
                   'indexKey': False, 'comment': 'in radians',
                   'unique': False}
        elev_def = {'name': 'elevation', 'type': float, 'length': 8,
                    'indexKey': False, 'comment': 'in meters',
                    'unique': False}
        xazm_def = {'name': 'Xazimuth', 'type': float, 'length': 8,
                    'indexKey': False, 'comment': 'in radians',
                    'unique': False}
        xalt_def = {'name': 'Xaltitude', 'type': float, 'length': 8,
                    'indexKey': False, 'comment': 'angle of x-arm radians',
                    'unique': False}
        yazm_def = {'name': 'Yazimuth', 'type': float, 'length': 8,
                    'indexKey': False, 'comment': 'in radians',
                    'unique': False}
        yalt_def = {'name': 'Yaltitude', 'type': float, 'length': 8,
                    'indexKey': False, 'comment': 'angle of y-arm: radians',
                    'unique': False}
        xmid_def = {'name': 'Xmidpoint', 'type': float, 'length': 8,
                    'indexKey': False, 'comment': 'in meters',
                    'unique': False}
        ymid_def = {'name': 'Ymidpoint', 'type': float, 'length': 8,
                    'indexKey': False, 'comment': 'in meters',
                    'unique': False}

        column_definitions = [id_def, name_def, dect_def, lat_def, lon_def,
                              elev_def, xazm_def, yazm_def, xalt_def, yalt_def,
                              xmid_def, ymid_def]
        eq_cols = [name_def, dect_def, lat_def, lon_def,
                   elev_def, xazm_def, yazm_def, xalt_def, yalt_def, xmid_def,
                   ymid_def]
        self.define_cols(column_definitions)
        self.set_eq_cols(eq_cols)
        return self.cols
