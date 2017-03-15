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

EXPORT_LIMIT = 500000
EXPORT_FILE_PRIMARY = '%s-primary'
EXPORT_FILE_FULL = '%s-full'

PROCESS_GENRES = ['rusrock', 'ukrrock', 'rock-n-roll', 'prog-rock', 'post-rock', 'new-wave', 'metal', 'rock']
ALL_ROCK_GENRE = 'rock-all'

PLOT_LAYOUT = 'fr'
