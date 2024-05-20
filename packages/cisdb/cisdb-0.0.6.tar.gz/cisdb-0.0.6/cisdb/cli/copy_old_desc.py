#!/usr/bin/env python
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

import time
import argparse
import logging
import os
import configparser

from cisdb.cis import CisDB
from cisdb.descriptionrow import Description
from basedb.database import Database

start_time = time.time()

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'copy_old_desc'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'


def abs_path(inpath):
    ret = os.path.abspath(inpath)
    return ret

def main():
    logging.basicConfig()
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    start_time = time.time()
    parser = argparse.ArgumentParser(description=__doc__,
                                     prog=__process_name__)
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('--old-config', type=abs_path, required=True,
                        help='Log in config for old DB')
    parser.add_argument('--config', type=abs_path, required=True,
                        help='Log in config for new DB')

    args = parser.parse_args()

    verbosity = args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    cisdb = CisDB(args.config)
    descriptiontable = cisdb.descriptiontable
    descriptiontable.create(ifnotexists=True)

    # manually deal with old db because just his once (fingers crossed)
    oldconfig = configparser.ConfigParser()
    oldconfig.read(args.old_config)
    olddb_args = dict(oldconfig['DATABASE'])
    olddb = Database(**olddb_args)

    descriptionlist = descriptiontable.read()
    descriptions = cisdb.rowlist2dict(descriptionlist, 'name', Description)
    newdesc = dict()
    upddesc = dict()

    # load the channel descriptions from old db the
    sql = 'SELECT name, `desc`,`text` FROM cis_channeldescription'
    cursor = olddb.execute_query(sql)
    for row_tup in cursor.fetchall():
        row_data = dict()
        name = row_tup[0]
        row_data['name'] = name
        row_data['descriptions'] = []
        desc = row_tup[1].strip()
        if desc:
            row_data['descriptions'].append(desc)
        txt = row_tup[2].strip()
        if txt:
            row_data['descriptions'].append(txt)
        if row_data['descriptions']:
            row = Description()
            row.set(row_data)
            if name in descriptions.keys():
                olddesc = descriptions[name]
                if olddesc.needs_update(row):
                    olddesc.merge(row)
                    if name in upddesc:
                        upddesc[name].merge(olddesc)
                    else:
                        upddesc[name] = olddesc
            elif name in newdesc:
                newdesc[name].merge(row)
            else:
                newdesc[name] = row
    cursor.close()

    # we put subsystem descriptions into same table
    sql = 'select name, description from cis_subsystem ' \
          'where length(label) > 0 and length(description) > 1'
    cursor = olddb.execute_query(sql)
    for row_tup in cursor.fetchall():
        row_data = dict()
        name = row_tup[0]
        row_data['name'] = name
        row_data['descriptions'] = []
        desc = row_tup[1].strip()
        if desc:
            row_data['descriptions'].append(desc)
            row = Description()
            row.set(row_data)
            if name in descriptions.keys():
                olddesc = descriptions[name]
                if olddesc.needs_update(row):
                    olddesc.merge(row)
                    if name in upddesc:
                        upddesc[name].merge(olddesc)
                    else:
                        upddesc[name] = olddesc
            elif name in newdesc:
                newdesc[name].merge(row)
            else:
                newdesc[name] = row

    if newdesc:
        newdesclist = list(newdesc.values())
        descriptiontable.insert(newdesclist)
    if (upddesc):
        upddesclist = list(upddesc.values())
        descriptiontable.update(upddesclist, 'name')

    elap = time.time() - start_time
    logger.info('run time {:.1f} s'.format(elap))

if __name__ == "__main__":
    main()