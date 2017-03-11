# -*- coding: utf-8 -*-

import os

DB_USER = 'ya'
DB_PSWD = 'ya'
DB_NAME = 'ya'

HOST = 'https://music.yandex.ru'
DISPLAY = True
DEBUG = False
CUSTOM_WAIT_TIMEOUT = (10, 35)
FIND_TIMEOUT = 20
REQUEST_TIMEOUT = 30
CHROME_DRIVER_PATH = os.path.sep.join([os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'chromedriver'])

DATA_FOLDER_PATH = os.path.sep.join([os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'data'])

GRAPH_EXPORT_LIMIT = 100000
ROCK_GRAPH_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'rock.gml'])
ROCK_GRAPH_PLOT_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'rock-%s.%s'])
ROCK_SIMILAR_GRAPH_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'rock-similar.gml'])
ROCK_SIMILAR_GRAPH_PLOT_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'rock-similar-%s.%s'])
