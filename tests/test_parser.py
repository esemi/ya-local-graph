# -*- coding: utf-8 -*-

import unittest
import os

from app.cli.serials_update import _prepare_serial_url
from app.cli.imdb_search import _prepare_imdb_search_url, _prepare_imdb_film_url
from app.models.parser import last_page_parser, search_page_parser, film_info_parser, serial_info_parser,\
    imdb_search_page_parser, imdb_film_page_parser
from app.models.db import get_genres


SOURCE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'source'))


def _get_source(num):
    return open(os.path.join(SOURCE_PATH, 'test_parser_%d.html') % num).read()


class LastPageFilmsSearchTest(unittest.TestCase):

    def test_not_found(self):
        res = last_page_parser('')
        self.assertIsNone(res)

    def test_valid_not_found(self):
        source = _get_source(5)
        res = last_page_parser(source)
        self.assertEqual(0, res)

    def test_valid_many_pages(self):
        source = _get_source(1)
        res = last_page_parser(source)
        self.assertEqual(16, res)

    def test_valid_single_page(self):
        source = _get_source(2)
        res = last_page_parser(source)
        self.assertEqual(1, res)


class SearchFilmsPageTest(unittest.TestCase):

    def test_not_found(self):
        res = search_page_parser('')
        self.assertIsNone(res)

    def test_valid_many_films(self):
        source = _get_source(3)
        res = search_page_parser(source)
        self.assertIsInstance(res, list)
        self.assertEquals(100, len(res))
        self.assertEquals(762381, res[0])

    def test_valid_empty_films(self):
        source = _get_source(4)
        res = search_page_parser(source)
        self.assertEqual([], res)


class FilmInfoPageTest(unittest.TestCase):
    def _check_film_fields(self, res):
        self.assertIsInstance(res, dict, msg=res)
        expected_keys = dict(film_id=None, name='', alt_name='', rank_kp=None, rank_imdb=None, genres=[], img_link=None,
                             runtime=None, movie_info=None, actors=None, country=None, year=None, director=None,
                             phrase=None, budget=None, age=None).keys()
        for k in expected_keys:
            self.assertIn(k, res.keys())

    def test_valid_regress_1(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/98784/', _get_source(22), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)

    def test_valid_basic(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/854942/', _get_source(6), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)

    def test_valid_ranking_hide(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/8098/', _get_source(8), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)
        self.assertIsNone(res['rank_kp'])

    def test_valid_ranking_imdb_not_found(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/854942/', _get_source(9), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)
        self.assertIsNone(res['rank_imdb'])

    def test_valid_empty_runtime(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/1183/', _get_source(11), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)
        self.assertIsNone(res['runtime'])

    def test_valid_empty_info(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/1183/', _get_source(11), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)
        self.assertIsNone(res['movie_info'])

    def test_valid_empty_actors(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/1494/', _get_source(12), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)
        self.assertIsNone(res['actors'])

    def test_valid_empty_country(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/6586/', _get_source(13), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)
        self.assertIsNone(res['country'])

    def test_valid_empty_year(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/726382/', _get_source(14), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)
        self.assertIsNone(res['year'])

    def test_valid_empty_director(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/1213/', _get_source(16), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)
        self.assertIsNone(res['director'])

    def test_valid_empty_phrase(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/1183/', _get_source(11), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)
        self.assertIsNone(res['phrase'])

    def test_valid_empty_budget(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/1183/', _get_source(11), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)
        self.assertIsNone(res['budget'])

    def test_valid_empty_age(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/911/', _get_source(18), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)
        self.assertIsNone(res['age'])

    def test_valid_small_poster(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/307/', _get_source(20), get_genres())
        self.assertIsInstance(res, dict)
        self._check_film_fields(res)
        self.assertEquals('https://st.kp.yandex.net/images/film_iphone/iphone360_307.jpg', res['img_link'])

    def test_empty(self):
        res = film_info_parser('', '', {})
        self.assertEquals('not create lxml document', res)

    def test_invalid_unicode(self):
        pass

    def test_invalid_film_id(self):
        res = film_info_parser('https://www.kinopoisk.ru/dfdf/1/', _get_source(6), {})
        self.assertEquals('not parsed film id', res)

    def test_invalid_names(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/1/', _get_source(7), get_genres())
        self.assertEquals('not parsed names', res)

    def test_invalid_runtime(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/1/', _get_source(10), get_genres())
        self.assertEquals('not parsed runtime', res)

    def test_invalid_year(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/1/', _get_source(15), get_genres())
        self.assertEquals('not parsed film year', res)

    def test_invalid_phrase(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/1/', _get_source(17), get_genres())
        self.assertEquals('not parsed phrase', res)

    def test_invalid_age(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/1/', _get_source(19), get_genres())
        self.assertEquals('not valid age found', res)

    def test_invalid_img(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/1/', _get_source(21), get_genres())
        self.assertEquals('not found img link', res)

    def test_invalid_genre(self):
        res = film_info_parser('https://www.kinopoisk.ru/film/1/', _get_source(6), {})
        self.assertEquals(u'found unknown genre боевик', res)


class SerialEpisodesPageTest(unittest.TestCase):
    maxDiff = 2048

    def _check_serial_fields(self, res):
        self.assertIsInstance(res, dict, msg=res)
        expected_keys = ['film_id', 'runtime', 'season_count', 'episodes']
        for k in expected_keys:
            self.assertIn(k, res.keys())

        expected_keys = ['episode_num', 'season_num', 'name', 'alt_name', 'date_string']
        self.assertIsInstance(res['episodes'], list, msg=res['episodes'])
        for single_episode in res['episodes']:
            self.assertIsInstance(single_episode, dict)
            for k in expected_keys:
                self.assertIn(k, single_episode.keys())

    def test_valid_source_case(self):
        res = serial_info_parser(_prepare_serial_url(464963), _get_source(23))
        self._check_serial_fields(res)
        self.assertEqual(464963, res['film_id'])
        self.assertEqual(8, res['season_count'])
        self.assertEqual(u'2 дня 18 часов 55 минут — 4015 мин.', res['runtime'])
        self.assertEqual(73, len(res['episodes']))
        self.assertSequenceEqual(set(range(1, 9)), set([int(tmp['season_num']) for tmp in res['episodes']]))

    def test_runtime_wo_film_signup_case(self):
        res = serial_info_parser(_prepare_serial_url(6722), _get_source(24))
        self._check_serial_fields(res)
        self.assertEqual(u'3 часа 45 минут — 225 мин.', res['runtime'])

    def test_runtime_miss_case(self):
        res = serial_info_parser(_prepare_serial_url(6720), _get_source(25))
        self._check_serial_fields(res)
        self.assertIs('', res['runtime'])

    def test_season_count_one_case(self):
        res = serial_info_parser(_prepare_serial_url(6720), _get_source(25))
        self._check_serial_fields(res)
        self.assertEqual(1, res['season_count'])

    def test_episode_wo_altname_case(self):
        res = serial_info_parser(_prepare_serial_url(6720), _get_source(25))
        self._check_serial_fields(res)
        etalon_res = [
            dict(episode_num=1, season_num=1, name='Gilded Youth', alt_name='', date_string=u'26 марта 1985'),
            dict(episode_num=2, season_num=1, name='Trials', alt_name='', date_string=u'27 марта 1985'),
            dict(episode_num=3, season_num=1, name='De Profundis', alt_name='', date_string=u'28 марта 1985')
        ]
        self.assertListEqual(etalon_res, res['episodes'])

    def test_episode_wo_season_case(self):
        res = serial_info_parser(_prepare_serial_url(9449), _get_source(26))
        self._check_serial_fields(res)
        self.assertEqual(31, len(res['episodes']))

    def test_season_empty_case(self):
        res = serial_info_parser(_prepare_serial_url(220052), _get_source(27))
        self._check_serial_fields(res)
        self.assertEqual(4, len(res['episodes']))

    def test_duplicate_episodes_case(self):
        res = serial_info_parser(_prepare_serial_url(439877), _get_source(28))
        self._check_serial_fields(res)
        self.assertEqual(262, len(res['episodes']))
        episode_keys = ['%s-%s' % (e['season_num'], e['episode_num']) for e in res['episodes']]
        self.assertEqual(262, len(episode_keys))
        self.assertEqual(262, len(set(episode_keys)))

    def test_episode_wo_name_case(self):
        res = serial_info_parser(_prepare_serial_url(432680), _get_source(29))
        self._check_serial_fields(res)
        self.assertEqual(20, len(res['episodes']))

    def test_invalid_empty_source(self):
        res = serial_info_parser(_prepare_serial_url(1), '')
        self.assertEqual('not create lxml document', res)

    def test_invalid_utf(self):
        pass

    def test_invalid_film_id(self):
        res = serial_info_parser('', _get_source(23))
        self.assertEqual('not parsed film id', res)

    def test_invalid_season_string(self):
        res = serial_info_parser(_prepare_serial_url(464963), _get_source(30))
        self.assertEqual('not parsed season string', res)

    def test_invalid_runtime(self):
        res = serial_info_parser(_prepare_serial_url(464963), _get_source(31))
        self.assertEqual('very long runtime string', res)

    def test_invalid_serial_episodes_empty(self):
        pass

    def test_invalid_serial_episodes_parse(self):
        pass

    def test_invalid_not_unique_episode(self):
        pass


class ImdbSearchPageTest(unittest.TestCase):
    def test_prepare_url_function(self):
        u_etalon = u'http://www.imdb.com/find?s=tt&exact=true&ref_=fn_tt_ex&kp_f_id=123&kp_f_year=1972&q=%D0%94%D0%BE%D0%B2%D0%B5%D1%80%D0%B8%D0%B5'
        res = _prepare_imdb_search_url(u'Доверие', 123, 1972)
        self.assertEquals(u_etalon, res)

    def test_unicode_unquote(self):
        import urllib
        etalon_name = u'Доверие йоба'
        url_q = urllib.quote_plus(etalon_name.encode('utf-8'))
        self.assertEquals('%D0%94%D0%BE%D0%B2%D0%B5%D1%80%D0%B8%D0%B5+%D0%B9%D0%BE%D0%B1%D0%B0', url_q)
        result_name = urllib.unquote_plus(url_q).decode('utf-8')
        self.assertEquals(etalon_name, result_name)

    def test_valid_w_year_case(self):
        res = imdb_search_page_parser(_prepare_imdb_search_url(u'Confidence', 123, 1980), _get_source(32))
        self.assertEquals(res, (123, '/title/tt0078868/?ref_=fn_tt_tt_2'))

    def test_valid_wo_year_case(self):
        res = imdb_search_page_parser(_prepare_imdb_search_url(u'Confidence', 123, None), _get_source(32))
        self.assertEquals(res, (123, '/title/tt0310910/?ref_=fn_tt_tt_1'))

    def test_valid_unicode_name(self):
        res = imdb_search_page_parser(_prepare_imdb_search_url(u'Доверие', 123, 1972), _get_source(32))
        self.assertEquals(res, (123, '/title/tt4686464/?ref_=fn_tt_tt_16'))

    def test_empty_source_case(self):
        res = imdb_search_page_parser(_prepare_imdb_search_url(u'Доверие', 123, 1972), '')
        self.assertEquals(res, 'not create lxml document')

    def test_invalid_url_case(self):
        res = imdb_search_page_parser(_prepare_imdb_search_url(u'Доверие', 0, 1972), _get_source(32))
        self.assertEquals(res, 'invalid url')

    def test_not_full_page_case(self):
        res = imdb_search_page_parser(_prepare_imdb_search_url(u'Доверие', 123, 1972), _get_source(33))
        self.assertEquals(res, 'not full page')

    def test_no_image_case(self):
        res = imdb_search_page_parser(_prepare_imdb_search_url(u'Confidence', 123, 1933), _get_source(32))
        self.assertEquals(res, 'not found film poster')

    def test_not_found_case(self):
        res = imdb_search_page_parser(_prepare_imdb_search_url(u'Смехуечки', 123, None), _get_source(32))
        res2 = imdb_search_page_parser(_prepare_imdb_search_url(u'Confidence', 123, 1911), _get_source(32))
        self.assertEquals(res, res2, 'not found film in serp')


class ImdbFilmPageTest(unittest.TestCase):
    def test_empty_source_case(self):
        res = imdb_film_page_parser(_prepare_imdb_film_url('/title/tt4686464/?ref_=fn_tt_tt_16', 123), '')
        self.assertEquals('not create lxml document', res)

    def test_invalid_url_case(self):
        res = imdb_film_page_parser(_prepare_imdb_film_url('/title/tt4686464/?ref_=fn_tt_tt_16', 0), _get_source(34))
        self.assertEquals('invalid url', res)

    def test_not_full_page_case(self):
        res = imdb_film_page_parser(_prepare_imdb_film_url('/title/tt4686464/?ref_=fn_tt_tt_16', 123), _get_source(35))
        self.assertEquals('not full page', res)

    def test_not_found_img_link_case(self):
        res = imdb_film_page_parser(_prepare_imdb_film_url('/title/tt4686464/?ref_=fn_tt_tt_16', 123), _get_source(36))
        self.assertEquals('not found img link', res)

    def test_valid(self):
        res = imdb_film_page_parser(_prepare_imdb_film_url('/title/tt4686464/?ref_=fn_tt_tt_16', 123), _get_source(34))
        self.assertEquals((123, 'https://images-na.ssl-images-amazon.com/images/M/MV5BMjM2Nzk4ODA2M15BMl5BanBnXkFtZTgwODA5MDExMDI@._V1_UX182_CR0,0,182,268_AL_.jpg'),
                          res)


if __name__ == '__main__':
    unittest.main()
