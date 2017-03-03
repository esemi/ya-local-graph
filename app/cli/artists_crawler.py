# -*- coding: utf-8 -*-

import re
import logging
import time
import os
import random

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from app import config


def custom_wait():
    time.sleep(random.randint(*config.CUSTOM_WAIT_TIMEOUT))


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
        self.driver.get('%s/genre/%s/artists' % (config.HOST, genre))

        artists = []
        page = 0
        while True:
            logging.info('parse %d page' % page)
            next_button = self.driver.find_element_by_xpath('//div[@class="pager"]//a[contains(@class, "button_pin_left")]')
            # self.driver.execute_script("return arguments[0].scrollIntoView();", next_button)
            new_artists = self.__fetch_all_artists()
            logging.info('found %d artists' % len(new_artists))
            if not new_artists:
                break
            artists += new_artists
            page += 1
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            next_button.click()
            custom_wait()

        logging.info('found %d artists total (pages %d)' % (len(artists), page))
        logging.info(artists)
        # save artists

    def __fetch_all_artists(self):
        res = []
        slots = self.driver.find_elements_by_xpath('//div[@class="page-genre__artists"]//div[@class="artist__content"]')
        for item in slots:
            try:
                link_elem = item.find_element_by_xpath('.//div[@class="artist__name"]/a')
                artist = {
                    'name': link_elem.get_attribute('title').strip(),
                    'id': int(re.findall(r'/artist/(\d+)', link_elem.get_attribute('href').strip())[0]),
                }
                logging.info('parse artist %s', artist)
                res.append(artist)
            except NoSuchElementException:
                logging.error('not parsed artist %s' % item.text)
        return res


def task(genre):
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    m = Manager()
    try:
        m.artist_crawling(genre)
        m.close()
    except Exception as e:
        logging.error('exception %s', e)
        if not config.DEBUG:
            m.close()
        raise e


