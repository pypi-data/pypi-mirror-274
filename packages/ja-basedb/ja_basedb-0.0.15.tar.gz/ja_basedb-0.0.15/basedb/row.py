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

"""Base class representing one row in a table"""

from basedb.column import Column

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__name__ = 'row'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'


class Row:

    def __init__(self):
        self.cols = dict()
        self.col_names = list()
        self.data = dict()
        self.eq_cols = list()

    def __str__(self):
        ret = '{}: {}'.format(type(self),
                              self.data if len(self.data) else self.col_names)
        return ret

    def isclose(self, a, b):
        """
        float version of ==
        :param a:
        :param b:
        :return: True if a is close enough to b
        """
        ret = abs(a - b) * 2 / abs(a + b) < 1e-6
        return ret

    def define_cols(self, definitions):
        """Column definitions are used to create tables and copy
        values to/from the DB

        :param definitions: list of dictionaries. See Column class
        :return: (cols, col_names)
            cols - list of Column objects
            col_names - list of column_names
        """
        for parm in definitions:
            name = parm['name']
            self.col_names.append(name)
            col = Column(**parm)
            coldef = col.get_column_def()
            assert (coldef is not None)
            self.cols[name] = col
        return self.cols, self.col_names

    def set_eq_cols(self, definitions):
        """
        List of column definitions used for equality test
        :param definitions: list of thw same definition dicts used for d
            define_cols
        :return: true if all named cols aew equal
        """
        self.eq_cols = definitions

    def set(self, vals):
        """
        Update row to have values needed for insert
        :param vals: Dictionary of column names -> value
        :return: self
        :raises AttributeError: if unknown column included or required column
        omitted
        """
        if not self.cols:
            self.get_col_def()
        bad_vals = list()
        missing = list()
        for valk in vals.keys():
            if valk in self.col_names:
                self.data[valk] = vals[valk]
            else:
                bad_vals.append(valk)

        for col in self.cols.values():
            if col.notNull or (col.primary and not col.autoIncrement):
                if col.name not in self.data.keys():
                    missing.append(col.name)

        if bad_vals or missing:
            ermsg = 'Problem initializing {} row: '.format(self.__name__)
            if bad_vals:
                ermsg += 'Unknown columns:' + ', '.join(bad_vals) + '  '
            if missing:
                ermsg += 'Missing required columns: ' + ', '.join(missing)
            raise AttributeError(ermsg)
        return self

    def get_col_def(self):
        """
        Get information needed to create all columns in this row
        :return: a list of dictionaries, see Column for dictionary description
        """
        pass

    def merge(self, other):
        """
        Merge 2 object, append new colums if list, add if unset,
        fail if they differ and not a list
        :param other: must be same subclass
        :return: this object updated so a.merge(b).merge(c) works
        :raises AttributeError: merge failed
        """
        if not self.cols:
            self.get_col_def()
        for k in other.data.keys():
            if k in self.data.keys():
                a = self.data[k]
                b = other.data[k]
                if not b:
                    continue
                if self.cols[k].type == list:
                    if not isinstance(a, list) and not isinstance(b, list):
                        if a != b:
                            self.data[k] = [a, b]
                    else:
                        if not isinstance(a, list):
                            a = [a]
                        if not isinstance(b, list):
                            b = [b]
                        if set(a) != set(b):
                            a += list(set(b) - set(a))
                            self.data[k] = a
                else:
                    if not isinstance(b, self.cols[k].type):
                        raise AttributeError('Row value for {} must '
                                             'be type {} not {}'.
                                             format(k, self.cols[k].type,
                                                    type(b)))
                    if not a:
                        self.data[k] = b
                    elif (self.cols[k].type == float and self.isclose(a, b)) \
                            or (self.cols[k].type == str and a.upper() == b.upper()) or (a == b):
                        pass
                    else:
                        raise AttributeError('Merge conflict for {}. {} != {}'.
                                             format(k, a, b))

        return self     # in case they want to merge multiple

    def get_insert_vals(self, col_names, db=None):
        """
        Return text to add to a bulk insert command
        :param db:
        :param col_names: which colums to return in order
        :return: str like '(val1, val2, ...)'
        """
        vals = ''
        for nam in col_names:
            if nam not in self.col_names:
                raise AttributeError('{} requested but a '
                                     'valid column'.format(nam))
            vals += ', ' if vals else ''
            if nam in self.data.keys():
                dbval = self.cols[nam].get_db_val(self.data[nam], db)
                vals += dbval
            else:
                vals += 'NULL'

        return vals

    def get_update_setter(self, db):
        """
        Generate the SET clause for an UPDATE statement.  All values in
        the data member except auto_increment and primary index fields
        are included.
        :return: None
        """
        ret = ''
        for key, col in self.cols.items():
            if col.autoIncrement or col.primary:
                continue
            name = col.name
            if name in self.data.keys():
                ret += ', ' if ret else ''
                ret += ' {} = {}'.\
                    format(name, col.get_db_val(self.data[name], db))
        return ret

    def get_where(self, id_col, db=None):
        """
        Return a test to identify this row by specified columnn
        :param id_col: name of the column to test
        :param db: Database object used to escape strings
        :return: atest eg: 'id=5' No where keyword
        """
        if id_col in self.cols.keys():
            ret = '{} = {}'.\
                format(id_col, self.cols[id_col].
                       get_db_val(self.data[id_col], db))
        else:
            raise AttributeError('Problem getting test for {}'.format(id_col))
        return ret

    def get_return_vals(self, col_name, db_val):
        """
        Decode our db special types like list
        :param col_name: which column
        :param db_val: value from database select statement
        :return: python version
        """
        ret = self.cols[col_name].get_ret_val(db_val)
        return ret

    def needs_update(self, other):
        """
        Note only the columns in the eq_cols list are tested. This allows
        a new row with only some fields to check if an update is needed.

        :param other: another row of the same type
        :return: True if no new info in other
        """
        nodiff = True
        for col_name in self.eq_cols:
            if col_name in self.data and col_name in other.data:
                col = self.cols[col_name]
                us = self.data[col_name]
                them = other.data[col_name]
                if us is not None and them is not None:
                    if col.type == list:
                        if not isinstance(them, list):
                            them = [them]
                        nodiff &= len(set(them) - set(us)) == 0
                    else:
                        nodiff &= us == them
                elif them and not us:
                    # we have a falsey thingy and they have real data
                    nodiff = False
                    break
            elif col_name not in self.data and col_name in other.data:
                # new datum seen
                nodiff = False
                break
        return not nodiff
