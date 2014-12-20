# -*- coding: utf-8 -*-
import os
from string import Template

HTMLDIR = "html"
TEMPLATEDIR = "html"

def get_file(directory, filename):
    path = os.path.join(directory, filename)
    return open(path, 'r').read()

def get_html(filename):
    return get_file(HTMLDIR, filename)

def get_template(filename):
    return Template(get_file(TEMPLATEDIR, filename))
