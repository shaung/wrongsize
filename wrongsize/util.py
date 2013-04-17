# coding: utf-8

import os
from datetime import datetime, date, time, timedelta
import itertools

try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict


def timeit(func):
    @wraps
    def f(*args, **kws):
        start = time.time()
        rslt =  func(*args, **kws)
        end = time.time()
        print end - start
        return rslt
    return f

def to_cp932(s):
    if isinstance(s, unicode):
        return s.encode('cp932')
    elif isinstance(s, str):
        try:
            us = s.decode('cp932')
        except:
            return s.decode('utf8').encode('cp932')
        else:
            return s
    else:
        return s

def unilen(s):
    if isinstance(s, unicode):
        try:
            return len(s.encode('cp932'))
        except:
            return len(s.encode('utf8'))
    else:
        return len(s)


class DATE:
    YMD = datetime.strftime(datetime.today(), '%Y%m%d')
    HMS = datetime.strftime(datetime.today(), '%H%M%S')
    NOW = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    TODAY = datetime.strftime(datetime.today(), '%Y-%m-%d')


def get_dates_between(start, end):
    days = (end + timedelta(days=1) - start).days
    return [start + timedelta(days=i) for i in range(days)]

def date_range(start, end):
    fromstr = lambda dt: datetime.strptime(dt, '%Y/%m/%d')
    return [datetime.strftime(dt, '%Y/%m/%d') for dt in get_dates_between(fromstr(start), fromstr(end))]

def time_range(count, dt, start, step):
    strd = '%s %s' % (dt, start)
    d = datetime.strptime(strd, '%Y/%m/%d %H:%M:%S')
    for i in range(count):
        d += timedelta(minutes=step)
        yield datetime.strftime(d, '%Y/%m/%d %H:%M:%S')


class Console(object):
    """ Redirect stdout to file"""
    def __init__(self, fpath=None):
        self.fpath = fpath
        if not self.fpath:
            self.output = StringIO()
        else:
            basedir = os.path.dirname(fpath)
            if not os.path.exists(basedir):
                try:
                    os.makedirs(basedir)
                except:
                    pass
            self.output = open(fpath, 'wb')
        self.old_stdout = sys.stdout
        sys.stdout = self.output

    def get(self):
        result = self.output.getvalue()
        return result

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        sys.stdout = self.old_stdout
        self.output.close()


def groupby(iterable, key):
    groups = OrderedDict({})
    iterable = sorted(iterable, key=key)
    for k, g in itertools.groupby(iterable, key):
        groups[k] = tuple(g)
    return groups
