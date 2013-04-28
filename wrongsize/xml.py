# -*- coding: utf-8 -*-

"""
    wrongsize.xml
    ~~~~~~~~~~~~~

    Xml parsing helpers.
"""

import os, sys
from lxml import etree

from StringIO import StringIO

import re


class XMLParser(object):
    """ Parser.  """

    def __init__(self, filepath):
        self.filepath = filepath


    def iterparse(self, tag, func, func_check=None):
        """ iterparsing the xml file.

        *tag: XML element tag
        *func: call back function
        *func_check: the node will get parsed only when this function returns True

        """
        context = etree.iterparse(self.filepath, events=(u'start', u'end'))
        event, root = context.next()
        for event, elem in context:
            if elem.tag != tag:
                continue

            if event == 'end' and (not func_check or func_check(elem)):
                func(elem)
                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
                root.clear()
                del event
                del elem
        del event
        del root
        del context
