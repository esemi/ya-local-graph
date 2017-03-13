# -*- coding: utf-8 -*-

import logging

from app.config import ROCK_PRIMARY_FILE, ROCK_FULL_FILE
from app.model import fetch_graph_primary, fetch_graph_full, get_genres
from app.cli.graph_plot import clear_cache


def save_gml(f_name, nodes, edges, directed=True, reset=False):
    logging.info('save fetch genre short %d %d', len(nodes), len(edges))
    f = open(f_name, 'w+')
    content = ['graph [']

    if directed:
        content.append('    directed 1')

    for id, attrs in nodes.items():
        content.append('    node [')
        content.append('        id %d' % id)
        for name, val in attrs.items():
            content.append('        %s "%s"' % (name, val.replace('"', '\'')))
        content.append('    ]')

    for from_id, to_id in edges:
        content.append('    edge [')
        content.append('        source %d' % from_id)
        content.append('        target %d' % to_id)
        content.append('    ]')

    content.append(']')

    f.write("\n".join(content))
    f.close()

    if reset:
        clear_cache(f_name)


def task(reset=False):
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    genres = get_genres()
    rock_ids = [str(genres[i]) for i in genres if i in {'rusrock', 'rock', 'ukrrock', 'rock-n-roll', 'prog-rock',
                                                        'post-rock', 'new-wave'}]

    logging.info('export primary rock %s', rock_ids)
    nodes, edges = fetch_graph_primary(rock_ids)
    save_gml(ROCK_PRIMARY_FILE, nodes, edges, reset=reset)
    logging.info('export primary rock end %d %d', len(nodes), len(edges))

    logging.info('export full rock %s', rock_ids)
    nodes, edges = fetch_graph_full(rock_ids)
    save_gml(ROCK_FULL_FILE, nodes, edges, reset=reset)
    logging.info('export full rock end %d %d', len(nodes), len(edges))


if __name__ == '__main__':
    task()
