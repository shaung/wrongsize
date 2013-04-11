# coding: utf-8

import os
import tempfile

from mako.template import Template
from mako.lookup import TemplateLookup

mod_dir = os.path.normpath(os.path.join(tempfile.gettempdir(), 'mako_modules/')) 

look = TemplateLookup(directories=[os.path.normpath('.')], module_directory=mod_dir,
       output_encoding='cp932', input_encoding='cp932', default_filters=['decode.cp932'])


class Template(object):
    def __init__(self, template):
        self.template = template

    def render_to_file(self, file_out, paras):
        rslt = self.template.render(**paras)
        f = open(file_out, 'wb') if isinstance(file_out, basestring) else file_out
        f.write(rslt)
        f.close()


def get_template(name):
    template = look.get_template(name)
    return Template(template)
