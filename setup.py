# coding: utf-8

__VERSION__ = '0.0.1'

import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

params = {
    'name': 'wrongsize',
    'version': __VERSION__,
    'description': 'whatever',
    'long_description': read('README.md'),
    'author': 'shaung',
    'author_email': 'shaun.geng@gmail.com',
    'url': 'https://github.com/shaung/wrongsize/',
    'packages': ['wrongsize'],
    'license': 'BSD',
    'download_url': '',
    'zip_safe': False,
    'classifiers': [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
}

from setuptools import setup
setup(**params)
