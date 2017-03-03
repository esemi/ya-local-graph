# -*- coding: utf-8 -*-

import re
import logging
import time
import os
import random

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from app import config
from app.model import save_new_artist


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

    def artist_crawling(self, genre, page):
        logging.info('run artist crawling %s %s' % (genre, page))
        self.driver.get('%s/genre/%s/artists?page=%d' % (config.HOST, genre, page))

        new_artists_count = 0
        while True:
            logging.info('parse %s url' % self.driver.current_url)
            new_artists = self.__fetch_all_artists()
            logging.info('found %d artists' % len(new_artists))
            if not new_artists:
                break

            for a in new_artists:
                r = save_new_artist(a['id'], a['name'])
                new_artists_count += int(r)
            logging.info('new %d artists' % new_artists_count)

            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            try:
                next_e = self.driver.find_element_by_xpath('//div[@class="pager"]'
                                                           '//a[contains(@class, "button_pin_left") and '
                                                           'not(contains(@class, "button_checked"))]')
            except NoSuchElementException:
                break

            next_e.click()
            custom_wait()

        logging.info('found %d new artists total' % new_artists_count)

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


def task(genre, page=0):
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    m = Manager()
    try:
        m.artist_crawling(genre, int(page))
        m.close()
    except Exception as e:
        logging.error('exception %s', e)
        if not config.DEBUG:
            m.close()
        raise e


