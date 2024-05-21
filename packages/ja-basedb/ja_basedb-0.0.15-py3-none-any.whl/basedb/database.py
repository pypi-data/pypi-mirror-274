#!/usr/bin/env python
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

"""Class wrapping a maridb connection"""
import re
import time
import logging

import mysql.connector


__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'db'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'


class Database:

    logger = None

    @staticmethod
    def get_logger():
        """
        Get a single logger used by all cisdb classes.
        Set the Database.logger variable if needed
        :return: a python logger object
        """
        if Database.logger is None:
            logging.basicConfig()
            Database.logger = logging.getLogger(__process_name__)
            Database.logger.setLevel(logging.DEBUG)
        return Database.logger

    def __init__(self, user=None, password=None, host=None,
                 database=None, port=None, dsn=None, logger=None):
        """Create a connection to the database
        INPUT:
            user:       username
            password:   password
            host:       db server host
            database:   db name
            dsn:        dictionary of connection parameters(data source name)
            logger:
        """
        cstrt = time.time()
        Database.logger = logger
        self.connection = None
        if dsn:
            config = dsn
        else:
            config = {'host': 'localhost'}
        if user:
            config['user'] = user
        if password:
            config['password'] = password
        if host:
            config['host'] = host
        if database:
            config['database'] = database
        if port:
            config['port'] = port

        self.connection = mysql.connector.connect(**config)
        con_time = time.time() - cstrt
        Database.get_logger().debug(f'DB connected to {config["database"]}@{config["host"]} as {config["user"]}. '
                                    f'{con_time:.3f}s')

    def get_table_list(self):
        """
        Get a list of all tables in this DB
        :return: a dictionary all tables, types
        """
        sql = 'SHOW FULL TABLES'
        curs = self.execute_query(sql)

        ret = dict()
        for (tbl, ttyp) in curs.fetchall():
            ret[tbl] = ttyp
        curs.close()
        return ret

    def execute(self, sql, commit=False):
        """Execute a sql statement that does not return a result set"""
        cursor = self.connection.cursor()
        cursor.execute(sql)
        if commit:
            self.connection.commit()
        cursor.close()

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def execute_query(self, sql):
        """Execute a sql query returning a cursor object.
        Don't forget to close it when finished."""
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor

    def close(self):
        """
        Close our connection if necessary
        :return: None
        """
        if self.connection:
            self.connection.close()
        self.connection = None

    def escape_str(self, instr):
        """
        Escape any special chars like single, double quotes
        :param instr: input string
        :return: escaped string as utf-8 string
        """
        ret = re.escape(instr)
        return ret

    def __del__(self):
        """ Make sure connection is closed when an object goes out of scope"""
        self.close()

    def cursor2list(self, cursor, columns):
        """
        convert results in a cursor to a list of dictionaries
        :param cursor: input cursor
        :return: list of dict's with all columns
        """
        ret = list()
        colnames = list()
        for d in cursor.description:
            colnames.append(d[0])

        for row_tup in cursor.fetchall():
            row_data = dict()
            for idx in range(0, len(colnames)):
                colname = colnames[idx]
                rval = columns[colname].get_ret_val(row_tup[idx])
                row_data[colname] = rval

            ret.append(row_data)
        return ret
