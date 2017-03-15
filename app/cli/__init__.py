# -*- coding: utf-8 -*-

import os

from app.config import DATA_FOLDER_PATH, EXPORT_FILE_PRIMARY, EXPORT_FILE_FULL


def cache_name(name):
    return '%s.layout' % name


def gml_name(name):
    return '%s.gml' % name


def plot_name(name, mod, extension):
    return '%s-%s.%s' % (name, mod, extension)


def graph_name(genre, full):
    template = EXPORT_FILE_FULL if full else EXPORT_FILE_PRIMARY
    return os.path.sep.join([DATA_FOLDER_PATH, template % genre])

