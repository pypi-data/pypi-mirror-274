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

"""Class representingthe ChannelInformation System's database
It's mainly a collection of high level functions"""

import configparser
from basedb.database import Database
from cisdb.channeltable import ChannelTable
from cisdb.fragmenttable import FragmentTable
from cisdb.ifotable import IfoTable
from cisdb.descriptionstable import Descriptions

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__myname__ = 'cis'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'


class CisDB:

    def __init__(self, config_path=None, host=None, user=None, password=None,
                 database=None):

        # if they give us a config file read it first
        config = configparser.ConfigParser()
        config.read(config_path)
        #: argument used to create the Database instance
        self.db_args = dict(config['DATABASE'])

        # Any other args override
        if host:
            self.db_args['host'] = host
        if user:
            self.db_args['user'] = user
        if password:
            self.db_args['password'] = password
        if database:
            self.db_args['database'] = database

        # get db and tables
        #: The Database instance
        self.db = Database(**self.db_args)
        #: A ChannelTable instance available fpr use
        self.channeltable = ChannelTable(self.db)
        #: A Fragment table instance available for use
        self.fragmenttable = FragmentTable(self.db)
        #: An IfoTable instance available for use
        self.ifotable = IfoTable(self.db)
        #: A Descriptions (table) instance available for use
        self.descriptiontable = Descriptions(self.db)

    def rowlist2dict(self, rows, key, myclass):
        """
        Convert list of dictionaries returned by db to
        dictionary of dictionaries
        :param rows: row objects returned by table.read
        :param key: which column to use as dict key
        :param myclass: class of the row
        :return: dictionary key ->row object
        """
        ret = dict()
        for row_data in rows:
            idk = row_data[key]
            row = myclass()
            row.set(row_data)
            ret[idk] = row
        return ret

    def add_upd_row(self, key, newrow, dbrows, newdict, upddict):
        """
        Figure out what to do with this row:
        a) ignore as already there, b) add as new, c) update existing
        :param key: for all dicts
        :param newrow: object containing the potential new row
        :param dbrows: dict key -> objects of what's in this db table
        :param newdict: where to add rows not in dbrows
        :param upddict: where to put rows that add to whats in db
        :return: newdict or upddict updated if needed
        """
        if key in dbrows:
            dbrow = dbrows[key]
            if dbrow.needs_update(newrow):
                dbrow.merge(newrow)
                if key in upddict.keys():
                    upddict[key].merge(newrow)
                else:
                    upddict[key] = newrow
        elif key in newdict:
            newdict[key].merge(newrow)
        else:
            newdict[key] = newrow

    def escape_str(self, instr):
        """
        Escape any special chars like single, double quotes
        :param instr: input string
        :return: escaped string
        """
        return self.db.escape_str(instr)
