# coding: utf-8

from nose.tools import eq_

import wrongsize as ws


def inspect_db():
    from wrongsize import db
    db.inspect()


def test_groupby():
    from wrongsize.util import groupby
    li = [
        ('A', 1),
        ('B', 4),
        ('A', 2),
        ('A', 3),
        ('B', 5),
    ]
    rslt = {
        'A' : (
            ('A', 1),
            ('A', 2),
            ('A', 3),
        ),
        'B' : (
            ('B', 4),
            ('B', 5),
        ),
    }
    eq_(rslt, groupby(li, lambda x: x[0]))


if __name__ == '__main__':
    inspect_db()
