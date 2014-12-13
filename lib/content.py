# -*- coding: utf-8 -*-
import os
from string import Template

CURDIR = os.path.dirname(os.path.abspath(__file__))
BASEDIR = os.path.join(CURDIR, "..")
HTMLDIR = os.path.join(BASEDIR, "html")
TEMPLATEDIR = os.path.join(BASEDIR, "html")
CSSDIR = os.path.join(BASEDIR, "html", "css")

def get_file(directory, filename):
    path = os.path.join(directory, filename)
    return open(path, 'r').read()

def get_html(filename):
    return get_file(HTMLDIR, filename)

def get_template(filename):
    return Template(get_file(TEMPLATEDIR, filename))

def get_css(filename):
    return get_file(CSSDIR, filename)
