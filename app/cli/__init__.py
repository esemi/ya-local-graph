# -*- coding: utf-8 -*-

import os

from app.config import DATA_FOLDER_PATH, EXPORT_FILE_PRIMARY, EXPORT_FILE_FULL


def gml_name(name):
    return '%s.gml' % name


def graph_index(genre, full):
    template = EXPORT_FILE_FULL if full else EXPORT_FILE_PRIMARY
    return template % genre


def graph_path(index):
    return os.path.sep.join([DATA_FOLDER_PATH, index])
