# -*- coding: utf-8 -*-

import logging
import os
import sys

from flask import Flask

from app.config import DefaultConfig, ProductionConfig, DevConfig

SERVICE_PATH = os.path.join(os.path.dirname(__file__), os.pardir)
APP_PATH = os.path.abspath(SERVICE_PATH)


def app_factory():
    app_instance = Flask(__name__)
    setup_config(app_instance)
    setup_logging(app_instance)
    return app_instance


def setup_logging(app):
    file_handler = logging.StreamHandler(sys.stdout)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    app.logger.addHandler(file_handler)
    if app.config['DEBUG']:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)


def setup_config(app):
    settings_map = {
        'dev': DevConfig,
        'prod': ProductionConfig,
    }

    env_file = os.path.join(APP_PATH, 'app.env')
    app_env = open(env_file).read().lower().strip()
    settings = settings_map[app_env]
    app.config.from_object(settings)


app = app_factory()

if not os.path.isdir(app.config['GRAPH_CACHE_DIR']):
    os.makedirs(app.config['GRAPH_CACHE_DIR'])

from app import views, config

