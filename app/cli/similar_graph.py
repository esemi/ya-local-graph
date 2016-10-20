# -*- coding: utf-8 -*-

import requests

from app import app


def search_artist(name):
    response = requests.request('GET', "https://music.yandex.ru/search",
                                params={'text': name, 'type': 'artists'},
                                timeout=15, allow_redirects=False)
    response.raise_for_status()
    with open('/tmp/ya-artist.html', 'wb') as f:
        f.write(response.content)


def task(root_artist_name=None, depth=3):
    """
    Task for search artist similar graph
    """
    with app.app_context():
        app.logger.info('cli task similar graph "%s" %s', root_artist_name, depth)
        if not root_artist_name:
            raise RuntimeError('Need send artist name')

        try:
            root_id = search_artist(root_artist_name)
        except Exception as e:
            raise RuntimeError('Not found root artist')


#       todo fetch root artist similar
#       todo fetch similar of similars recursive on depth
#       todo save local graph
#       todo generate image
