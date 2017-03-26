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
TOP_POSTFIX = '-top3'
EXPORT_FILE_PRIMARY = '%s-primary'
EXPORT_FILE_FULL = '%s-full'

ROCK_GENRES = ['rusrock', 'ukrrock', 'rock-n-roll', 'prog-rock', 'post-rock', 'new-wave', 'rock']
METAL_GENRES = ['metal', 'classicmetal', 'progmetal', 'Numetal', 'epicmetal', 'folkmetal', 'extrememetal']

PROCESS_GENRES = ROCK_GENRES + METAL_GENRES
ALL_ROCK_GENRE = 'rock-all'
ALL_METAL_GENRE = 'metal-all'
ROCK_AND_METAL_GENRE = 'summary'

PLOT_LAYOUT = 'fr'
