# -*- coding: utf-8 -*-

import os

DB_USER = 'ya'
DB_PSWD = 'ya'
DB_NAME = 'ya'

HOST = 'https://music.yandex.ru'
DISPLAY = True
DEBUG = False
CUSTOM_WAIT_TIMEOUT = (5, 25)
FIND_TIMEOUT = 8
REQUEST_TIMEOUT = 15
CHROME_DRIVER_PATH = os.path.sep.join([os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'chromedriver'])

DATA_FOLDER_PATH = os.path.sep.join([os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'data'])

GRAPH_EXPORT_LIMIT = 1000
SHORT_GRAPH_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'short.gml'])
FULL_GRAPH_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'full.gml'])
SHORT_GRAPH_PLOT_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'short%s.png'])
FULL_GRAPH_PLOT_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'full%s.png'])
