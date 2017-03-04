# -*- coding: utf-8 -*-

import logging

from app import config
from .artists_crawler import Manager


def task():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    m = Manager()
    try:
        m.similar_crawling()
        m.close()
    except Exception as e:
        logging.error('exception %s', e)
        if not config.DEBUG:
            m.close()
        raise e


