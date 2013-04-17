# coding: utf-8

import sys
import settings

try:
    settings.load_default()
except:
    print >> sys.stderr, 'Settings not found'
