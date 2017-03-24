# -*- coding: utf-8 -*-

import re
import logging
import time
import os
import random
from collections import Counter

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from app import config
from app.model import save_new_artist, get_artists_for_crawling_similar, update_crawled_similar_state, \
    save_similar_edge, update_degree, add_genre, update_artist_genres, get_genres, clear_similar_edges, \
    set_to_crawling_similar, get_similar


def custom_wait():
    time.sleep(random.randint(*config.CUSTOM_WAIT_TIMEOUT))


class Manager(object):

    _genres = get_genres()

    def __init__(self):
        os.environ["webdriver.chrome.driver"] = config.CHROME_DRIVER_PATH
        self._start()

    def _start(self):
        self.driver = webdriver.Chrome(executable_path=config.CHROME_DRIVER_PATH)
        self.driver.set_page_load_timeout(config.REQUEST_TIMEOUT)
        self.driver.implicitly_wait(config.FIND_TIMEOUT)

    def close(self):
        if self.driver:
            self.driver.quit()

    def restart(self):
        self.close()
        self._start()

    def similar_crawling(self, genre, reset_degree=False):
        logging.info('run similar crawling %s', genre)

        genres = genre.split(',')
        set_to_crawling_similar(genres)
        logging.info('set for crawling by genre %s', genres)

        cnt = Counter()
        start_time = time.time()

        artists = get_artists_for_crawling_similar()
        logging.info('fetch %d artists for crawling similar', len(artists))
        for artist in artists:
            logging.info('crawl %s %s artist similar', artist.id, artist.name)

            cnt['nodes_total'] += 1
            try:
                self.driver.get('%s/artist/%d/similar' % (config.HOST, artist.id))
                try:
                    self.driver.find_element_by_xpath('//div[contains(@class, "page-artist__title-similar")]')
                except NoSuchElementException:
                    cnt['invalid_page'] += 1
                    logging.warning('invalid page title')
                    continue

                last_tab = self.driver.find_elements_by_xpath('//div[contains(@class, "page-artist__tabs")]'
                                                              '//div[contains(@class, "tabs__tab")]')[-1]
                if 'tabs__tab_current' not in last_tab.get_attribute('class'):
                    cnt['empty_page'] += 1
                    logging.info('empty page')
                else:
                    similar_artists = self.__fetch_all_artists()
                    logging.info('found %d similar artists', len(similar_artists))
                    cnt['relations'] += len(similar_artists)
                    if len(similar_artists):
                        clear_similar_edges(artist.id)
                    else:
                        exist = get_similar(artist.id)
                        if len(exist):
                            logging.warning('not found already saved similar %d', len(exist))

                    for pos, a in enumerate(similar_artists):
                        r = save_new_artist(a['id'], a['name'])
                        cnt['new_artists'] += int(r)
                        update_artist_genres(a['id'], a['genres'])
                        save_similar_edge(artist.id, a['id'], pos)

                update_crawled_similar_state(artist.id, True)
                cnt['nodes_parsed'] += 1
            except Exception as e:
                cnt['fail'] += 1
                logging.warning('exception %s', e)
                continue
            finally:
                if cnt['nodes_total'] % 10 == 0:
                    logging.info('loop %s | v=%.2f artist/sec', cnt, cnt['nodes_total'] / (time.time() - start_time))

                if cnt['nodes_total'] % 200 == 0:
                    self.restart()

        logging.info('end %s', cnt)

        if reset_degree:
            update_degree()
            logging.info('compute degree')

    def artist_crawling(self, genre, page):
        logging.info('run artist crawling %s %s', genre, page)

        self.driver.get('%s/genre/%s/artists?page=%d' % (config.HOST, genre, page))

        new_artists_count = 0
        while True:
            logging.info('parse %s url', self.driver.current_url)
            new_artists = self.__fetch_all_artists()
            logging.info('found %d artists', len(new_artists))
            if not new_artists:
                break

            for a in new_artists:
                r = save_new_artist(a['id'], a['name'], True)
                new_artists_count += int(r)
                update_artist_genres(a['id'], a['genres'])
            logging.info('new %d artists', new_artists_count)

            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            try:
                next_e = self.driver.find_element_by_xpath('//div[@class="pager"]'
                                                           '//a[contains(@class, "button_pin_left") and '
                                                           'not(contains(@class, "button_checked"))]')
            except NoSuchElementException:
                break

            next_e.click()
            custom_wait()

        logging.info('found %d new artists total', new_artists_count)

    def __fetch_all_artists(self):
        res = []
        slots = self.driver.find_elements_by_xpath('//div[@class="page-genre__artists" or @class="page-artist__artists"]'
                                                   '//div[@class="artist__content"]')
        for item in slots:
            try:
                link_elem = item.find_element_by_xpath('.//div[@class="artist__name"]/a')
                genre_links = item.find_elements_by_xpath('.//div[@class="artist-summary"]/a')
                genre_names = set([re.findall(r'/genre/(.+)', i.get_attribute('href').strip())[0] for i in genre_links])
                genre_ids = []
                for g in genre_names:
                    try:
                        id = self._genres[g]
                    except KeyError:
                        logging.info('add genre %s', g)
                        id = add_genre(g)
                        self._genres[g] = id
                    genre_ids.append(id)

                artist = {
                    'name': link_elem.get_attribute('title').strip(),
                    'id': int(re.findall(r'/artist/(\d+)', link_elem.get_attribute('href').strip())[0]),
                    'genres': genre_ids
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


