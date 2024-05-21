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


"""Example: how to search for channels"""
from pathlib import Path

from cisdb.cis import CisDB
from cisdb.descriptionrow import Description
import logging
import os

from flask import Flask, request
from ja_webutils.Page import Page
from ja_webutils.PageItem import PageItemHeader
from ja_webutils.PageTable import PageTable, PageTableRow, RowType

try:
    from ._version import __version__
except ImportError:
    __version__ = 'unknown'

app = Flask(__name__)


__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__myname__ = 'ChannelSearch'

logging.basicConfig()
logger = logging.getLogger(__myname__)
logger.setLevel(logging.DEBUG)

page = Page()
page.add(PageItemHeader('Sample CIS web page', 2))
# open a database connection
etc = Path(__file__).parent.parent / 'etc'
configfile = etc / 'cisdb.ini'
if configfile.exists():
    logger.debug('Using configuration: {}'.format(configfile))
else:
    logger.critical(f'Expected configuration file ({configfile.absolute()} not found')
    exit(3)
cisdb = CisDB(configfile)

# Get a specific channel ignoring IFO
name = 'gds-calib_strain'
rows = cisdb.channeltable.read(where='name=\'{}\''.format(name))
page.add_blanks(2)
page.add(f'Searching for {name}')
for row in rows:
    for item in row.items():
        print('{}: {}'.format(item[0], item[1]))

# Try to get a description that does not exist
name = 'not-a_real_channel'
rows = cisdb.descriptiontable.read(where='name=\'{}\''.format(name))
logger.debug('return from read failure: {}'.format(rows))

# one with text
name = 'HPI-BS_BLND_L4C_RX_IN1_DQ'
rows = cisdb.descriptiontable.read(['name', 'descriptions'],
                                   where='name=\'{}\''.format(name))
for row in rows:
    for item in row.items():
        print('{}: {}'.format(item[0], item[1]))

# add a description
cisdb.descriptiontable.insert_update_desc('GRD', 'Guardian subsystemXX')

# add another detail
cisdb.descriptiontable.insert_update_desc('GRD', 'Guardian is a finite state '
                                                 'machine that is used to '
                                                 'control the interferometer.')

# fix the typo
rows = cisdb.descriptiontable.read(['name', 'descriptions'],
                                   where='name=\'grd\'')
for row_data in rows:
    new_desc = []
    for desc in row_data['descriptions']:
        if 'subsystemXX' in desc:
            new_desc.append(desc.replace('subsystemXX', 'subsystem'))
        else:
            new_desc.append(desc)
    row_data['descriptions'] = new_desc
    row = Description()
    row.set(row_data)
    cisdb.descriptiontable.update(row, 'name')

print(page.get_html())