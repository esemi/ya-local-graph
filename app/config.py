# -*- coding: utf-8 -*-

import os

DB_USER = 'ya'
DB_PSWD = 'ya'
DB_NAME = 'ya'

HOST = 'https://music.yandex.ru'
DISPLAY = True
DEBUG = False
CUSTOM_WAIT_TIMEOUT = (5, 20)
FIND_TIMEOUT = 10
REQUEST_TIMEOUT = 20
CHROME_DRIVER_PATH = os.path.sep.join([os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'chromedriver'])

DATA_FOLDER_PATH = os.path.sep.join([os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'data'])

GRAPH_EXPORT_LIMIT = 1000000
ROCK_PRIMARY_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'rock-primary.gml'])
ROCK_PRIMARY_PLOT_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'rock-primary-%s.%s'])
ROCK_FULL_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'rock-full.gml'])
ROCK_FULL_PLOT_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'rock-full-%s.%s'])

METAL_PRIMARY_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'metal-primary.gml'])
METAL_PRIMARY_PLOT_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'metal-primary-%s.%s'])
METAL_FULL_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'metal-full.gml'])
METAL_FULL_PLOT_FILE = os.path.sep.join([DATA_FOLDER_PATH, 'metal-full-%s.%s'])
