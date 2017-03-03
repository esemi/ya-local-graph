# -*- coding: utf-8 -*-

import os

DEBUG = True
CUSTOM_WAIT_TIMEOUT = (5, 15)
FIND_TIMEOUT = 15
REQUEST_TIMEOUT = 15
CHROME_DRIVER_PATH = os.path.sep.join([os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'chromedriver'])
HOST = 'https://music.yandex.ru'
DISPLAY = True
