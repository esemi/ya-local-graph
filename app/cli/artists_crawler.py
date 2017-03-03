# -*- coding: utf-8 -*-

import logging
import time
import os

from selenium import webdriver

from app import config


def custom_wait():
    time.sleep(config.CUSTOM_WAIT_TIMEOUT)


class Manager(object):

    def __init__(self):
        os.environ["webdriver.chrome.driver"] = config.CHROME_DRIVER_PATH
        self.driver = webdriver.Chrome(executable_path=config.CHROME_DRIVER_PATH)
        self.driver.set_page_load_timeout(config.REQUEST_TIMEOUT)
        self.driver.implicitly_wait(config.FIND_TIMEOUT)

    def close(self):
        if self.driver:
            self.driver.quit()

    def artist_crawling(self, genre):
        logging.info('run artist crawling %s' % genre)


def task(genre):
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    m = Manager()
    try:
        m.artist_crawling(genre)
    except Exception as e:
        logging.error('exception %s', e)
        raise e
    finally:
        if not config.DEBUG:
            m.close()


