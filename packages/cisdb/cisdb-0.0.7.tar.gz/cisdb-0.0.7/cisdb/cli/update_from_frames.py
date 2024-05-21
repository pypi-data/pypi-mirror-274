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

"""Update channels, ifos, and fragments tables from frame files"""

import time

start_time = time.time()

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'update_from_frames'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

import argparse
import logging

import os
import re

from LDAStools import frameCPP

from cisdb.cis import CisDB
from cisdb.channelrow import ChannelRow
from cisdb.fragmentrow import FragmentRow
from cisdb.iforow import IfoRow

# the following dictionaries are channel name (no ifo) -> Channel row object
# newXXX to be inserted, updXXX to be updated
newifo = dict()
updifo = dict()

newfrag = dict()
updfrag = dict()

newchan = dict()
updchan = dict()

subsystems = set()
fragments=set()

global ifos, logger, cisdb, chans

type2str = {
    frameCPP.FrVect.FR_VECT_C: 'CHAR',
    frameCPP.FrVect.FR_VECT_2S: 'INT_2S',
    frameCPP.FrVect.FR_VECT_4S: 'INT_4S',
    frameCPP.FrVect.FR_VECT_8S: 'INT_8S',
    frameCPP.FrVect.FR_VECT_4R: 'REAL_4',
    frameCPP.FrVect.FR_VECT_8R: 'REAL_8',
    frameCPP.FrVect.FR_VECT_8C: 'COMPLEX_8',
    frameCPP.FrVect.FR_VECT_16C: 'COMPLEX_16',
    frameCPP.FrVect.FR_VECT_STRING: 'STRING',
    frameCPP.FrVect.FR_VECT_1U: 'CHAR_U',
    frameCPP.FrVect.FR_VECT_2U: 'INT_2U',
    frameCPP.FrVect.FR_VECT_4U: 'INT_4U',
    frameCPP.FrVect.FR_VECT_8U: 'INT_8U',
}


def abs_path(path):
    ret = os.path.abspath(path)
    return ret


def add_detector(detector):
    global ifos, logger, newifo, updifo
    ifo_vals = dict()
    ifo_vals['detector'] = detector.GetName()
    name = detector.GetPrefix()
    name = name[0:2]
    ifo_vals['name'] = name
    ifo_vals['latitude'] = detector.GetLatitude()
    ifo_vals['longitude'] = detector.GetLongitude()
    ifo_vals['elevation'] = detector.GetElevation()
    ifo_vals['Xazimuth'] = detector.GetArmXazimuth()
    ifo_vals['Xaltitude'] = detector.GetArmXaltitude()
    ifo_vals['Yazimuth'] = detector.GetArmYazimuth()
    ifo_vals['Yaltitude'] = detector.GetArmYaltitude()
    ifo_vals['Xmidpoint'] = detector.GetArmXmidpoint()
    ifo_vals['Ymidpoint'] = detector.GetArmYmidpoint()
    ifo = IfoRow()
    ifo.set(ifo_vals)
    if (name in ifos and ifo == ifos[name]) or \
       (name in newifo and ifo == newifo[name]):
        pass
    else:
        if name in ifos:
            ifo.merge(ifos[name])
            if name in updifo:
                ifo.merge(updifo[name])
            updifo[name] = ifo
        if name in newifo:
            newifo[name].merge(ifo)
        else:
            newifo[name] = ifo


def add_adc(stream, adc_Iist, frame_type):
    """
    Divide channels into duplicates, updates, new
    :param stream: the open frameCPP  stream
    :param adc_Iist: list of channel names
    :param frame_type: type to add to definition
    :return: globals newchan and updcan dictionaries updated
    """
    global logger
    if frame_type.endswith('_T'):
        ctype = 's-trend'
        istrend = True
    elif frame_type.endswith('_M'):
        ctype = 'm_trend'
        istrend = True
    elif frame_type.endswith('_RDS'):
        ctype = 'reduced'
        istrend = False
    else:
        ctype = 'raw'
        istrend = False
    logger.info('Frame: {}, chtype: {}, is Trend: {}'.
                format(frame_type, ctype, istrend))

    for chname in adc_Iist:
        if istrend:
            if not chname.lower().endswith('.mean'):
                continue

        chrow = ChannelRow()
        adc_data = stream.ReadFrAdcData(0, chname)
        adc_name = adc_data.GetName()
        if chrow.parse_name(adc_name):
            base_name = chrow.data['name']
            rdata = {
                'chan_types': ctype,
                'slope': adc_data.GetSlope(),
                'xoffset': adc_data.GetBias(),
                'frames': frame_type
            }
            for frvect in adc_data.data:
                add_frvects(rdata, frvect)

            chrow.set(rdata)
            cisdb.add_upd_row(base_name, chrow, chans, newchan, updchan)


def add_frvects(rdata, frvect):
    dim = frvect.GetDim(0)
    dx = dim.GetDx()
    if dx > 0:
        fs = 1 / dx
        if 'sample_rates' in rdata.keys():
            fss = rdata['sample_rates']
            if not isinstance(fss, list):
                fss = [fss]
            fss.append(fs)
        else:
            fss = [fs]
        rdata['sample_rates'] = fss

    dtype_code = frvect.GetType()
    if dtype_code in type2str:
        dtype = type2str[dtype_code]
    else:
        dtype = 'unknown'

    if 'data_types' in rdata.keys():
        dtypes = rdata['data_types']
        if not isinstance(dtypes, list):
            dtypes = [dtypes]
        dtypes.append(dtype)
    else:
        dtypes = [dtype]
    rdata['data_types'] = dtypes
    rdata['unitX'] = dim.GetUnitX()
    rdata['unitY'] = frvect.GetUnitY()


def add_proc(stream, proc_list, frame_type):
    """
    Add or update all processed channels in this frame file
    :param stream:
    :param proc_list:
    :return:
    """
    global logger

    if frame_type.endswith('_T'):
        ctype = 's-trend'
        istrend = True
    elif frame_type.endswith('_M'):
        ctype = 'm_trend'
        istrend = True
    else:
        ctype = 'reduced'
        istrend = True

    for chname in proc_list:
        if istrend:
            if not chname.endswith('.mean'):
                continue
            else:
                chname = chname.replace('.mean', '')
        chrow = ChannelRow()
        proc_data = stream.ReadFrProcData(0, chname)
        ptype = proc_data.GetType()
        if ptype != frameCPP.FrProcData.TIME_SERIES:
            continue
        chrow.parse_name(proc_data.GetName())
        base_name = chrow.data['name']

        rdata = {
            'chan_types': ctype,
            'frames': frame_type
        }
        for frvect in proc_data.data:
            add_frvects(rdata, frvect)

        chrow.set(rdata)
        cisdb.add_upd_row(base_name, chrow, chans, newchan, updchan)


def main():
    global ifos, logger, cisdb, chans, newifo, updifo

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
    parser.add_argument("--gwf", type=abs_path, nargs='+',
                        help="path to one or more GWF file")
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

    # debugging?
    logger.debug(f'{__process_name__} version: {__version__} called with arguments:')
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    cisdb = CisDB(args.config)
    channeltable = cisdb.channeltable
    fragmenttable = cisdb.fragmenttable
    ifotable = cisdb.ifotable

    if args.reset:
        channeltable.drop(ifexists=True)
        fragmenttable.drop(ifexists=True)
        ifotable.drop(ifexists=True)

    channeltable.create(ifnotexists=True)
    fragmenttable.create(ifnotexists=True)
    ifotable.create(ifnotexists=True)

    ldstrt = time.time()
    chanList = channeltable.read(order='name')
    chans = cisdb.rowlist2dict(chanList, 'name', ChannelRow)

    logger.info('{} channels loaded from db in {:.1f} s'.
                format(len(chans), time.time() - ldstrt))

    ifolist = ifotable.read(order='name')
    ifos = cisdb.rowlist2dict(ifolist, 'name', IfoRow)
    logger.info('{} IFOs loaded from db in {:.1f} s'.
                format(len(ifos), time.time() - ldstrt))

    for gwf in args.gwf:
        b1 = os.path.basename(gwf)
        m = re.search('(.+)[-_]\\d+-\\d+.gwf', b1)
        frame_type = 'n/a'
        if m:
            frame_type = m.group(1)
        logger.info('Processing {}, frame type: {}'.format(gwf, frame_type))
        stream = frameCPP.IFrameFStream(str(gwf))
        nframes = stream.GetNumberOfFrames()
        if nframes == 1:
            toc = stream.GetTOC()
        else:
            stream2 = stream.ReadNextFrame()
            toc = stream.GetTOC()

        detectornames = toc.GetNameDetector()

        for detectorname in list(detectornames):
            add_detector(stream.ReadDetector(detectorname))

        adcList = toc.GetADC()
        if adcList:
            print('{} ADC channels'.format(len(adcList)))
            add_adc(stream, list(adcList.keys()), frame_type)

        procList = toc.GetProc()
        if procList:
            print('{} PROC channels'.format(len(procList)))
            add_proc(stream, procList, frame_type)

    logger.info('{} new IFOs found.'.format(len(newifo)))
    if newifo:
        ifos = list(newifo.values())
        ifotable.insert(ifos)

    logger.info('{} updated IFOs found.'.format(len(updifo)))
    if updifo:
        ifos = list(updifo.values())
        ifotable.update(ifos, 'name')

    logger.info('{} new channels found.'.format(len(newchan)))
    if newchan:
        chans = list(newchan.values())
        channeltable.insert(chans, commit=True)

    logger.info('{} updated channels found.'.format(len(newifo)))
    if updchan:
        chans = list(updchan.values())
        channeltable.update(chans, 'name')

    logger.info('{} new fragments found.'.format(len(newfrag)))
    if newfrag:
        frags = list(newfrag.values())
        fragmenttable.insert(frags)

    logger.info('{} updated fragments found.'.format(len(updfrag)))
    if updfrag:
        frags = list(updfrag.values())
        fragmenttable.update(frags, 'name')

    elap = time.time() - start_time
    logger.info('run time {:.1f} s'.format(elap))

if __name__ == "__main__":
    main()