# coding: utf-8

import os
import yaml

__CONF_PATH = os.getenv('WRONGSIZE_SETTINGS_PATH') or os.path.expanduser('~/_wrongsize')

def load(f):
    conf = yaml.load(f)
    globals().update(conf)

def load_default():
    with open(__CONF_PATH, 'rb') as f:
        load(f)
