import os
from string import Template

CURDIR = os.path.dirname(os.path.abspath(__file__))
BASEDIR = os.path.join(CURDIR, "..")
HTMLDIR = os.path.join(BASEDIR, "html")
TEMPLATEDIR = os.path.join(BASEDIR, "html")

def get_template(filename):
    path = os.path.join(TEMPLATEDIR, filename)
    return Template(open(path, 'r').read())

def get_html(filename):
    path = os.path.join(HTMLDIR, filename)
    return open(path, 'r').read()
