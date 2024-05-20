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

"""Class representing the data in a row of the channel table"""

import re
from basedb.row import Row

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'


class ChannelRow(Row):
    """Class representing the data in a row of the channel table"""

    def __init__(self, values=None):
        super().__init__()
        self.__name__ = 'ChannelRow'
        self.id = 0
        self.name = ''
        self.chan_types = []
        self.data_type = []
        self.ifo = ''
        self.subsystem = ''
        self.fragments = []
        self.sample_rate = []
        self.gain = 1.0
        self.slope = 1.0
        self.xoffset = 0.0
        self.current = False

    def get_col_def(self):
        id_def = {'name': 'id', 'type': int, 'autoincrement': True,
                  'length': 4,
                  'primary': True, 'comment': 'internal id number'}
        name_def = {'name': 'name', 'type': str, 'length': 100, 'indexKey':
                    True, 'comment': 'Channel name', 'unique': True,
                    'notNull': True}
        ctype_def = {'name': 'chan_types', 'type': list, 'length': 200,
                     'indexKey': False, 'unique': False,
                     'comment': 'JSON array of channel types'}
        dtype_def = {'name': 'data_types', 'type': list, 'length': 200,
                     'indexKey': False, 'unique': False,
                     'comment': 'JSON array of data types'}
        clstr_def = {'name': 'cluster', 'type': list, 'length': 200,
                     'indexKey': False, 'unique': False,
                     'comment': 'JSON array of NDS data locations'}
        frtyp_def = {'name': 'frames', 'type': list, 'length': 200,
                     'indexKey': False, 'unique': False,
                     'comment': 'JSON array of frame types'}
        ifo_def = {'name': 'ifo', 'type': list, 'length': 64,
                   'indexKey': True, 'comment': 'Interferometer',
                   'unique': False}
        subsys_def = {'name': 'subsystem', 'type': str, 'length': 64,
                      'indexKey': True, 'unique': False,
                      'comment': 'Sub-system (first fragment)'}
        frag_def = {'name': 'fragments', 'type': list, 'length': 200,
                    'indexKey': False, 'unique': False,
                    'comment': 'JSON array of fragments'}
        samp_rat_def = {'name': 'sample_rates', 'type': list, 'length': 200,
                        'indexKey': False, 'unique': False,
                        'comment': 'JSON array of sample rates'}
        unity_def = {'name': 'unitY', 'type': list, 'length': 200,
                     'indexKey': True, 'unique': False,
                     'comment': 'Units of Y-values'}
        unitx_def = {'name': 'unitX', 'type': list, 'length': 200,
                     'indexKey': True, 'unique': False,
                     'comment': 'Units of X-values'}
        gain_def = {'name': 'gain', 'type': list, 'length': 200,
                    'indexKey': False, 'unique': False,
                    'comment': 'Gain if data is linearly calibrated'}
        slope_def = {'name': 'slope', 'type': list, 'length': 200,
                     'indexKey': False, 'unique': False,
                     'comment': 'Slope if data is linearly calibrated'}
        xoffset_def = {'name': 'xoffset', 'type': list, 'length': 200,
                       'indexKey': False, 'unique': False,
                       'comment': 'Offset if data is linearly calibrated'}
        current_def = {'name': 'is_current', 'type': str, 'length': 1,
                       'indexKey': False, 'unique': False,
                       'comment': 'T/F is channel currently acquired'}

        column_definitions = [id_def, name_def, ctype_def, dtype_def, ifo_def,
                              subsys_def, frag_def, clstr_def, samp_rat_def,
                              unitx_def, unity_def, frtyp_def,
                              gain_def, slope_def, xoffset_def, current_def]

        self.define_cols(column_definitions)
        self.eq_cols = ['name', 'data_types', 'chan_types', 'frames', 'ifo',
                        'sample_rates', 'unitY', 'unitX', 'gain', 'slope',
                        'offset']
        return self.cols

    def parse_name(self, iname):
        """
        get ifo, base_name, and fragments from name
        :param iname: external full name eg 'H1:GDS-CALIB_STRAIN'
        :return: True if valid name and object fields were 1updated
        """
        name = iname.upper()
        ret = False
        # maybe they give us a trend channel name
        m = re.search('\\.(MIN|MAX|N|RMS|MEAN)', name)
        if m:
            name = name.replace('.' + m.group(1), '')

        if ':' in name:
            ifo_split = name.split(':')
            ifo = ifo_split[0]
            rest = ifo_split[1]

            if '-' in ifo:
                rest = ifo + '_' + rest
                ifo = ifo[0] + '0'

            name = rest
            tname = name
            for sep in '-_':
                tname = tname.replace(sep, ',')
            flist = tname.split(',')
            if len(flist) > 1:
                self.data['ifo'] = ifo
                self.data['name'] = name
                self.data['subsystem'] = flist[0]
                self.data['fragments'] = flist[1:]
                ret = True
        return ret
