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

"""Class representing a database table column"""

import json

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'
__name__ = 'column'

from pathlib import Path


class Column:
    def __init__(self, **kwargs):
        self.name = None
        self.type = None
        self.length = None
        self.notNull = None
        self.indexKey = None
        self.identity = None
        self.defaultVal = None
        self.unique = None
        self.autoIncrement = None
        self.comment = None
        self.primary = None

        for key in kwargs.keys():
            if key == 'name':
                self.name = kwargs[key]
            elif key == 'type':
                self.type = kwargs[key]
            elif key == 'length':
                self.length = kwargs[key]
            elif key == 'notNull':
                self.notNull = kwargs[key]
            elif key == 'indexKey':
                self.indexKey = kwargs[key]
            elif key == 'defaultVal':
                self.defaultVal = kwargs[key]
            elif key == 'unique':
                self.unique = kwargs[key]
            elif key == 'autoincrement':
                self.autoIncrement = kwargs[key]
            elif key == 'comment':
                self.comment = kwargs[key]
            elif key == 'primary':
                self.primary = True
            else:
                raise ValueError('Unknown column parameter {}'.format(key))

    def str(self):
        """
        Return a description of this object
        :return: short string
        """
        ret = '{}: {} {} {}'.\
            format(type(self), self.name, self.type, self.length)
        return ret

    def get_dbtype(self):
        """Convert python type and length to mariadb data type
        see: https://mariadb.com/kb/en/data-types/"""
        ret = None

        if self.type == int:
            if self.length == 1:
                ret = 'TINYINT'
            elif self.length == 2:
                ret = 'SMALLINT'
            elif self.length == 3:
                ret = 'MEDIUMINT'
            elif self.length == 4:
                ret = 'INTEGER'
            else:
                ret = 'BIGINT'
        elif self.type == float:
            if self.length and self.length <= 4:
                ret = 'FLOAT'
            else:
                ret = 'DOUBLE'
        elif self.type == str or self.type == list or self.type == Path:
            if self.length <= 128:
                ret = 'CHAR({:d})'.format(self.length)
            elif self.length < 256:
                ret = 'TINYTEXT'
            elif self.length < 65536:
                ret = 'TEXT'
            elif self.length < 16777216:
                ret = 'MEDIUMTEXT'
            else:
                ret = 'LONGTEXT'
        elif isinstance(self.type, str):
            typ = self.type.lower()
            if typ == 'date':
                ret = 'DATE'
            elif typ == 'time':
                ret = 'TIME'
            elif typ == 'time':
                ret = 'TIME'
            elif typ == 'timestamp':
                ret = 'TIMESTAMP'
            elif typ == 'blob':
                if self.length < 65536:
                    ret = 'BLOB'
                elif self.length < 16777216:
                    ret = 'MEDIUMBLOB'
                else:
                    ret = 'LONGBLOB'
        else:
            raise ValueError('Unknown column type {}'.format(self.type))
        return ret

    def get_column_def(self):
        """
        Get the SQL clause to define this column
        see https://mariadb.com/kb/en/create-table/#column-definitions
        :return: the definition
        """
        ret = ' {:s} '.format(self.name)
        dbtype = self.get_dbtype()
        ret += dbtype + ' '
        if self.notNull or self.primary:
            ret += ' NOT NULL '
        if self.autoIncrement:
            ret += ' AUTO_INCREMENT '
        if self.unique:
            ret += ' UNIQUE '
        if self.defaultVal:
            ret += ' DEFAULT "{:s}" '.format(self.defaultVal)
        if self.comment:
            ret += ' COMMENT "{:s}" '.format(self.comment)

        dbt = dbtype.lower()
        if (self.indexKey or self.primary) and not ('text' in dbt or 'blob' in dbt):
            primtxt = 'PRIMARY ' if self.primary else ''
            uniqtxt = 'UNIQUE' if self.unique else ''
            ret += ', {0:s} {1:s} KEY (`{2:s}`) '.format(primtxt, uniqtxt, self.name)

        return ret

    def get_text_blob_index(self):
        dbt = self.get_dbtype().lower()
        if ('text' in dbt or 'blob' in dbt) and self.indexKey:
            txtlen = 64 if self.length < 128 else 128
            u = 'UNIQUE' if self.unique else ''
            ret = '{} {:s} ({:d})'.format(u, self.name, txtlen)
        else:
            raise AttributeError('get_text_blob_index: {} is not a '
                                 'blob or text key'.
                                 format(self.name))
        return ret

    def get_db_val(self, val, db=None):
        """Convert python type and length to mariadb data type
        see: https://mariadb.com/kb/en/data-types/
        :param db: """
        ret = None

        if self.type == int or self.type == float:
            ret = '{}'.format(val)
        elif self.type == str:
            ret = '\'{}\''.format(val)
        elif self.type == list:
            if isinstance(val, list):
                vall = val
            else:
                vall = [val]
            jsonval = json.dumps(vall)
            if db:
                jsonval = db.escape_str(jsonval)
            ret = '\'{}\''.format(jsonval)
        elif isinstance(self.type, str):
            typ = self.type.lower()
            if typ == 'date' or typ == 'time' or typ == 'timestamp':
                ret = '\'{}\''.format(val)
            elif typ == 'blob':
                raise AttributeError('Joe does not know how to add blobs '
                                     'to insert statements do you?')
        elif self.type == Path:
            ret = f"'{str(Path(val).absolute())}'"
        else:
            raise ValueError('Unknown column type {}'.format(self.type))
        return ret

    def get_ret_val(self, db_val):
        if self.type == list and db_val:
            ret = json.loads(db_val)
        else:
            ret = db_val
        return ret
