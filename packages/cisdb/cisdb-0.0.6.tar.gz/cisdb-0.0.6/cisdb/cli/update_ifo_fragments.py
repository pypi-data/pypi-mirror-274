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

"""Scan channel table update ifo an fragment tables"""

import time

start_time = time.time()

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'update_ifo_fragments'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

import argparse
import logging
import os

from cisdb.cis import CisDB

from cisdb.fragmentrow import FragmentRow
from cisdb.iforow import IfoRow


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
    parser.add_argument('-c', '--config', type=abs_path, required=True,
                        nargs='+', help='Configuration file(s)')
    parser.add_argument('-r', '--reset', action='store_true', default=False,
                        help='completely rebuild the channel table')

    args = parser.parse_args()

    verbosity = args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    cisdb = CisDB(args.config)
    channeltable = cisdb.channeltable

    fragmenttable = cisdb.fragmenttable
    ifotable = cisdb.ifotable

    if args.reset:
        fragmenttable.drop(ifexists=True)
        ifotable.drop(ifexists=True)
    channeltable.create(ifnotexists=True)
    fragmenttable.create(ifnotexists=True)
    ifotable.create(ifnotexists=True)

    oldifo = dict()
    oldfrag = dict()
    newifo = dict()
    newfrag = dict()
    updifo = dict()
    updfrag = dict()

    chans = channeltable.read(cols=['ifo', 'fragments'])
    ifos = ifotable.read()
    for ifo in ifos:
        oldifo[ifo['name']] = ifo
    frags = fragmenttable.read()
    for frag in frags:
        oldfrag[frag['name']] = frag

    logger.info('{} channels read {:.2f} s elapsed'.
                format(len(chans), time.time() - start_time))

    for chan in chans:
        cifos = chan['ifo']
        for cifo in cifos:
            if cifo not in oldifo:
                newifo[cifo] = 1
        frags = chan['fragments']
        for frag in frags:
            if frag not in oldfrag:
                newfrag[frag] = 1

    logger.info('{} new IFO, {} new fragments found. {:.2f} s elapsed'.
                format(len(newifo), len(newfrag), time.time() - start_time))

    rows = list()
    for ifo in newifo:
        row = IfoRow()
        row.set({'name': ifo})
        rows.append(row)

    if len(rows) > 0:
        ifotable.insert(rows)
        logger.info('{} new IFOs inserted.{:.2f} s elapsed'.
                    format(len(newifo), time.time() - start_time))

    rows = list()
    for frag in newfrag:
        row = FragmentRow()
        row.set({'name': frag})
        rows.append(row)

    if len(rows) > 0:
        fragmenttable.insert(rows)
        logger.info('{} new fragments inserted.{:.2f} s elapsed'.
                    format(len(newfrag), time.time() - start_time))

    elap = time.time() - start_time
    logger.info('run time {:.1f} s'.format(elap))


if __name__ == "__main__":
    main()