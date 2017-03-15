# -*- coding: utf-8 -*-

import logging

from app.cli import graph_name, gml_name
from app.cli.graph_plot import clear_cache
from app.config import PROCESS_GENRES, ALL_ROCK_GENRE
from app.model import fetch_graph_primary, fetch_graph_full, get_genres


def save_gml(genre_name, nodes, edges, full=False):
    logging.info('save fetch genre  %d %d', len(nodes), len(edges))

    g_name = graph_name(genre_name, full)
    f_name = gml_name(g_name)
    f = open(f_name, 'w+')

    content = ['graph [']
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

    clear_cache(g_name)


def task():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    genres = get_genres()

    for genre_name in PROCESS_GENRES:
        genre_ids = [genres[genre_name]]
        logging.info('export primary %s %s', genre_name, genre_ids)
        nodes, edges = fetch_graph_primary(genre_ids)
        save_gml(genre_name, nodes, edges)
        logging.info('export primary end')

        logging.info('export full %s %s', genre_name, genre_ids)
        nodes, edges = fetch_graph_full(genre_ids)
        save_gml(genre_name, nodes, edges, full=True)
        logging.info('export full end')

    # all rock
    rock_ids = [str(genres[i]) for i in genres if i in {'rusrock', 'rock', 'ukrrock', 'rock-n-roll', 'prog-rock',
                                                        'post-rock', 'new-wave'}]
    logging.info('export primary rock-all %s', rock_ids)
    nodes, edges = fetch_graph_primary(rock_ids)
    save_gml(ALL_ROCK_GENRE, nodes, edges)
    logging.info('export primary end')
    logging.info('export full rock-all %s', rock_ids)
    nodes, edges = fetch_graph_full(rock_ids)
    save_gml(ALL_ROCK_GENRE, nodes, edges, full=True)
    logging.info('export full end')


if __name__ == '__main__':
    task()
