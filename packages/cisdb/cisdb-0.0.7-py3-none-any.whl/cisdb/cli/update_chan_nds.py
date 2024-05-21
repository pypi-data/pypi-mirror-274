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

"""Download all channels from NDS and update  the CIS database"""

import time
import argparse
import logging
import re
import os
import socket
import sys

from multiprocessing import Process, Queue, Value, Manager
from subprocess import Popen, PIPE, run

from cisdb.cis import CisDB

from cisdb.channelrow import ChannelRow
from cisdb.iforow import IfoRow
from cisdb.fragmentrow import FragmentRow

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'update_chan_nds'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

# Globals
sites = ['', 'ligo-la', 'ligo-wa']
ctypes = ['online', 'reduced', 'raw', 'm-trend', 's-trend', 'static']

xfer_q = Queue()            # tuples (site, ctype) defining each xfer
success = Value('i', 0)     # count of successful xfers
fail = Value('i', 0)        # count of faild xfers
tot_data = Value('f', 0)    # total size (bytes) of xfers
chan_lists = None           # dictionary of tuples: ChannelRow objects
cols = None                 # list of column objects
col_names = None            # list pf column names
db = None                   # database to use

# newXXX to be inserted, updXXX to be updated
newifo = dict()
updifo = dict()

newfrag = dict()
updfrag = dict()

newchan = dict()
updchan = dict()


def abs_path(inpath):
    ret = os.path.abspath(inpath)
    return ret


def get_chan_list(mypid=0):
    """
    Use NDS2 to transfer a channel list, run as a separate process
    :param mypid:
    :return:
    """
    global chan_lists
    while True:
        mysite, chtype = xfer_q.get()
        if mysite == 'stop':
            break
        else:
            if mysite:
                server = 'nds.{}.caltech.edu'.format(mysite)
                cluster = 'LHO' if mysite == 'ligo-wa' else 'LLO'
            elif 'ligo.caltech.edu' in socket.getfqdn():
                server = 'nds.ldas.cit'
                cluster = 'CIT'
            else:
                server = 'nds.ligo.caltech.edu'
                cluster = 'CIT'

            logger.info('{}: get_chan_list: {}, {}'.
                        format(mypid, server, chtype))

        try:
            cntcmd = ['nds_query', '-n', server, '-k', '-t', chtype]
            if 'trend' in chtype:
                cntcmd.append('*.mean')
            cntproc = Popen(cntcmd, stderr=PIPE, stdout=PIPE)
            cnt_stat = cntproc.wait(timeout=60)
            stdout, stderr = cntproc.communicate()

            if cnt_stat != 0:
                logger.warning('{}: error getting channel count from {}\n{}'.
                               format(mypid, server, stderr))
                continue

            m = re.search('(\\d+)', str(stdout))
            if m:
                nchan = int(m.group(1))
                logger.info('{:d}: {:s} has {:d}  {:s} channels'.
                            format(mypid, server, nchan, chtype))
            else:
                logger.info('{:d}: {:s} No {:d} channels found'.
                            format(mypid, server, chtype))
                continue

            lstcmd = ['nds_query', '-n', server, '-l', '-t', chtype]
            if 'trend' in chtype:
                lstcmd.append('*.mean')
            lst_stat = run(lstcmd, text=True, stdout=PIPE, stderr=PIPE)

            if lst_stat.returncode != 0:
                logger.warning('{}: error getting channel list from {}\n{}'.
                               format(mypid, server, lst_stat.stderr))
                continue

            for line in lst_stat.stdout.split('\n'):
                m = re.search('([^\\s]+)\\s+(\\d+)\\s+([^\\s]+)\\s+([^\\s]+)', line)
                if m:
                    try:
                        row = ChannelRow()
                        name = m.group(1).upper()
                        if 'trend' in chtype and 'mean' not in name:
                            continue
                        if not row.parse_name(name):
                            logger.warning('Rejecting {} as bad channel name'.format(name))
                            continue

                        data = {'sample_rates': float(m.group(2)), 'chan_types': m.group(3).upper(),
                                'data_types': m.group(4).upper(), 'cluster': cluster
                                }
                        row.set(data)
                        base_name = row.data['name']
                        cisdb.add_upd_row(base_name, row, chans, newchan, updchan)
                    except Exception as ex:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        logger.warning('{}: server {}, exception raised '
                                       'adding channel:\n    {}\n    {}'.
                                       format(mypid, server, str(ex),
                                              exc_traceback.format_exc()))
        except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.warning('{}: server {}, exception raised  '
                           'while getting channel list:\n    {}\n    {}'.
                           format(mypid, server, str(ex),
                                  exc_traceback.format_exc()))
            continue

    logger.info('{}: finished'.format(mypid))


def main():
    start_time = time.time()

    logging.basicConfig()
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description=__doc__,
                                     prog=__process_name__)
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('-p', '--proc', type=int,
                        default=len(sites) * len(ctypes),
                        help='Number of parallel transfers/parsers')
    parser.add_argument('-c', '--config', type=abs_path, required=True,
                        nargs='+', help='Configuration file(s)')
    parser.add_argument('-r', '--reset', action='store_true', default=False,
                        help='completely rebuild the channel table')
    parser.add_argument('-t', '--chan-type', nargs='*', type=str,
                        help='One or more channel types [raw, reduced, '
                             'm-trend, s-trend, static]')
    args = parser.parse_args()

    verbosity = args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    logger.info('Number of processes: {}'.format(args.proc))

    cisdb = CisDB(args.config)
    channeltable = cisdb.channeltable
    ifotable = cisdb.ifotable
    fragtable = cisdb.fragmenttable

    if args.reset:
        channeltable.drop(ifexists=True)
        ifotable.drop(ifexists=True)
        fragtable.drop(ifexists=True)

    channeltable.create(ifnotexists=True)
    ifotable.create(ifnotexists=True)
    fragtable.create(ifnotexists=True)

    ldstrt = time.time()
    chanList = channeltable.read(order='name')
    chans = cisdb.rowlist2dict(chanList, 'name', ChannelRow)

    logger.info('{} channels from db in {:.1f} s'.format(len(chans), time.time() - ldstrt))

    processes = []
    if args.chan_type:
        ctypes = args.chan_type

    for ctype in ctypes:
        for site in sites:
            xfer_q.put((site, ctype))

    qlen = len(ctypes) * len(sites)
    for q in range(0, qlen):
        xfer_q.put(('stop', 'stop'))

    nproc = max(min(qlen, args.proc), 1)
    if nproc == 1:
        logger.info("Multiprocessing disabled")
        chan_lists = dict()
        get_chan_list()
    else:
        logger.info('Using {} processes'.format(args.proc))
        manager = Manager()
        chan_lists = manager.dict()

        for t in range(0, nproc):
            p = Process(target=get_chan_list, args=(t,))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

    for srv, typ in chan_lists:
        in_chans = chan_lists[(srv, typ)]

    logger.info('{} new channels found.'.format(len(newchan)))
    if newchan:
        chans = list(newchan.values())
        channeltable.insert(chans)

    logger.info('{} updated channels found.'.format(len(updchan)))
    if updchan:
        chans = list(updchan.values())
        channeltable.update(chans, 'name')

    ldstrt = time.time()
    chanList = channeltable.read(order='name')
    chans = cisdb.rowlist2dict(chanList, 'name', ChannelRow)
    ifoList = ifotable.read(order='name')
    ifos = cisdb.rowlist2dict(ifoList, 'name', IfoRow)
    fragList = fragtable.read(order='name')
    frags = cisdb.rowlist2dict(fragList, 'name', FragmentRow)
    logger.info('{} channels, {} fragments, {} ifos loaded '
                'from db in {:.1f} s'.
                format(len(chans), len(frags), len(ifos),
                       time.time() - ldstrt))

    for chan in chanList:
        cifos = chan['ifo']
        for cifo in cifos:
            if cifo not in ifos:
                newifo[cifo] = 1

        frags = chan['fragments']
        for frag in frags:
            if frag not in newfrag:
                newfrag[frag] = 1

    logger.info('{} new IFOs found.'.format(len(newifo)))
    if newifo:
        rows = list()
        for ifo in newifo:
            row = IfoRow()
            row.set({'name': ifo})
            rows.append(row)

        if len(rows) > 0:
            ifotable.insert(rows)

    logger.info('{} new Fragments found.'.format(len(newfrag)))
    if newfrag:
        rows = list()
        for frag in newfrag:
            row = FragmentRow()
            row.set({'name': frag})
            rows.append(row)

        if len(rows) > 0:
            fragtable.insert(rows)

    elap = time.time() - start_time
    logger.info('run time (after imports) {:.1f} s'.format(elap))


if __name__ == "__main__":
    main()