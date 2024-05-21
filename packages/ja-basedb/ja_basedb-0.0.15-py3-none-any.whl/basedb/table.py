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

"""Base class representing a Mariadb/Mysql table"""

from basedb.row import Row

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__name__ = 'table'
try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'


class Table:

    def __init__(self, db, name, **kwargs):
        self.db = db
        self.columns = list()
        self.comment = ''
        self.name = name
        self.row_class = type(Row)
        self.temporary = None
        self.row = None

        for key in kwargs.keys():
            low_key = key.lower()
            if low_key == 'columns':
                self.columns = kwargs[key]
                self.col_names = list(self.columns.keys())
            elif low_key == 'comment':
                self.comment = kwargs[key]
            elif low_key == 'temporary':
                self.temporary = kwargs[key]
        self.row_class = type(self.row_class)
        if self.row:
            self.row_class = type(self.row)

    def create(self, ifnotexists=False):
        """Using the definitions from init creat a new table in the db"""
        sql = 'CREATE {0:s} TABLE {1:s} {2:s} ('.\
            format(('TEMPORARY' if self.temporary else ''),
                   ('IF NOT EXISTS' if ifnotexists else ''), self.name)
        if len(self.columns) == 0:
            raise ValueError('trying to create table {} but '
                             'no columns defined'.format(self.name))
        cdef = ''
        for col in self.columns.keys():
            cdef += ', ' if cdef else ''
            cdef += self.columns[col].get_column_def()
        sql += cdef + ')'

        self.db.execute(sql)
        # we need to create indexes to blob or text columns separately
        for col in self.columns.values():
            dbt = col.get_dbtype().lower()
            if ('text' in dbt or 'blob' in dbt) and col.indexKey:
                sql = 'CREATE INDEX {} {} ON {} ({})'.\
                    format(('IF NOT EXISTS' if ifnotexists else ''),
                           col.name, self.name, col.get_text_blob_index())
                self.db.execute(sql)

    def drop(self, ifexists=False):
        sql = 'DROP TABLE {} {}'.format('IF EXISTS' if ifexists else '',
                                        self.name)
        self.db.execute(sql)

    def get_column_list(self):
        """Get description of each column in this table"""
        sql = 'SHOW FULL COLUMNS FROM {}'.format(self.name)
        curs = self.db.execute_query(sql)
        ret = list()
        for (Field, Type, Collation, canBeNull, Key, colDefault, Extra, Privileges, Comment) in curs.fetchall():
            col = {"Field": Field, "Type": Type, "Collation": Collation,
                   "Null": canBeNull, "Key": Key, "Default": colDefault,
                   "Extra": Extra, "Privileges": Privileges,
                   "Comment": Comment}
            ret.append(col)
        curs.close()
        return ret

    def get_count(self):
        """
        Get record (row) count from this table
        :return: count as an int
        """
        sql = 'SELECT COUNT(*) AS count FROM {}'.format(self.name)
        curs = self.db.execute_query(sql)
        row = curs.fetchone()
        cnt = int(row[0])
        return cnt

    def insert(self, rows, commit=True):
        """
        Insert one or more rows into this table.
        Note all rows should have same keys in data dict as only keys in first
        row will be written
        :param rows: a single row or list of rows
        param
        :return: None
        """
        if isinstance(rows, list) and len(rows) > 0:
            # bulk insert
            prefix = 'INSERT INTO {} '.format(self.name)
            col_names = list(rows[0].data.keys())
            prefix += ' ({}) VALUES \n'.format(', '.join(col_names))
            vals = ''
            nrows = len(rows)
            if nrows > 1:
                # batch insert
                self.db.execute(f'ALTER TABLE {self.name} DISABLE KEYS;')
            for row in rows:
                if vals:
                    vals += ',\n'
                v = row.get_insert_vals(col_names, self.db)
                vals += '({})'.format(v)
                if len(vals) > 20000:
                    stmt = f'{prefix} {vals}'
                    self.db.execute(stmt, commit=commit)
                    vals = ''

            if len(vals) > 0:
                stmt = f'{prefix} {vals}'
                self.db.execute(stmt, commit=commit)
            if nrows > 1:
                self.db.execute(f'ALTER TABLE {self.name} ENABLE KEYS;')
        else:
            stmt = 'INSERT INTO {} '.format(self.name)
            col_names = list(rows.data.keys())
            stmt += ' ({}) VALUES \n'.format(', '.join(col_names))
            stmt += '({})'.format(rows.get_insert_vals(col_names))
            self.db.execute(stmt, commit=commit)

    def read(self, **kwargs):
        """
        Alias for select for backwards compatibility
        :param kwargs: see select
        :return: see select
        """
        self.db.logger.warning('Table.read is deprecated. Use select')
        return self.select(**kwargs)

    def select(self, cols=None, where=None, order=None, limit=None):
        """
        Construct and execute query of this table
        :param cols: None = all columns, single column name or
                     list of column names
        :param where: SQL where clause tests (no WHERE keyword)
        :param order: SQL ORDER BY clause
        :param limit: single vlaue or "offset, limit"
        :return: list of dictionaries (can be huge)
        """
        if cols:
            if isinstance(cols, list):
                cspec = ', '.join(cols)
            else:
                cspec = cols
        else:
            cspec = '*'

        stmt = f'SELECT {cspec} FROM {self.name} '
        if where:
            stmt += ' WHERE {} '.format(where)
        if order:
            stmt += ' ORDER BY {} '.format(order)
        if limit:
            stmt += ' LIMIT {} '.format(limit)

        cursor = self.db.execute_query(stmt)
        ret = self.db.cursor2list(cursor, self.columns)

        return ret

    def count(self, where=None):
        sql = 'SELECT COUNT(*) AS cnt FROM {} '.format(self.name)
        if where:
            sql += ' WHERE {} '.format(where)
        cursor = self.db.execute_query(sql)
        ret = 0
        for cnt in cursor:
            ret = int(cnt[0])
        cursor.close()
        return ret

    def update(self, rows, id_col_name):
        """
        Update one or more rows
        :param rows: individual or list of basedb.Row objects to update
        :param id_col_name: name of the column to identify row
        :return: None
        """
        if isinstance(rows, list):
            rlist = rows
        else:
            rlist = [rows]

        for row in rlist:
            setter = row.get_update_setter(self.db)
            where = row.get_where(id_col_name, self.db)
            stmt = 'UPDATE {} SET {} WHERE {}'.\
                format(self.name, setter, where)
            self.db.execute(stmt, commit=True)
