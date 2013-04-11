# coding: utf-8

import sys
import os
import pickle
from datetime import datetime, date, time

from sqlalchemy import create_engine, MetaData, Table as DBTable
from sqlalchemy.engine import reflection

import settings


dbengine = None
dbmeta = None
inspector = None

def inspect():
    global dbengine, inspector, dbmeta
    dbengine = create_engine(settings.DB_URI)
    inspector = reflection.Inspector.from_engine(dbengine)

    if os.path.exists(settings.DB_META_FILE):
        with open(settings.DB_META_FILE, 'rb') as f:
            dbmeta = pickle.load(f)
    else:
        dbmeta = MetaData()
        for table_name in inspector.get_table_names():
            print table_name
            table = DBTable(table_name, dbmeta, autoload=True, autoload_with=dbengine)
        for table_name in inspector.get_view_names():
            print table_name
            table = DBTable(table_name, dbmeta, autoload=True, autoload_with=dbengine)
        with open(settings.DB_META_FILE, 'wb') as f:
            pickle.dump(dbmeta, f)

    dbmeta.bind = dbengine


class TableBase(object):
    """ Table"""

    _cache = {}

    def __init__(self, table_name):
        self.table_name = table_name
        self._parse_prefix()
        self.table = DBTable(table_name, dbmeta, autoload=True, autoload_with=dbengine)

    def _parse_prefix(self):
        if table_name[:3].lower() == 'tav':
            self.prefix = ''
        elif table_name.startswith('V_'):
            self.prefix = ''
        else:
            self.prefix = table_name[:7]

    def get_short_name(self):
        return self.table_name[2:7].upper()

    def __getattr__(self, name):
        try:
            return getattr(self.table, name)
        except:
            if not name.startswith(self.prefix):
                name = '%s%s' % (self.prefix, name) if self.prefix else name
            return getattr(self.table.c, name)

    @classmethod
    def find(cls, table_name):
        if table_name in cls._cache:
            self = cls._cache[table_name]
        else:
            self = cls(table_name)
            cls._cache[table_name] = self
        return self

    def get_colname_list(self, with_prefix=False):
        cols = [str(x).split('.')[-1] for x in self.table.c]
        if not with_prefix and self.prefix:
            cols = [x[len(self.prefix):] for x in cols]
        return cols

    def cnt(self, cond=None):
        if cond is None:
            return self.count().execute().fetchone()[0]
        else:
            return self.count(cond).execute().fetchone()[0]

    def new(self, kws, conn=None):
        if self.prefix:
            values = dict((k.upper() if k.startswith(self.prefix) else (self.prefix + k.upper()), v) for k, v in kws.iteritems())
        else:
            values = kws
        stmt = self.insert().values(**values)
        return conn.execute(stmt) if conn is not None else stmt.execute()

    def getone(self, *args):
        pks = inspector.get_pk_constraint(self.table_name)['constrained_columns']
        cond = reduce((lambda x, y: x & y), ((x == y) for (x, y) in zip((getattr(self.table.c, x) for x in pks) , args)))
        return self.table.select(cond).execute().fetchone()


if __name__ == '__main__':
    inspect()
