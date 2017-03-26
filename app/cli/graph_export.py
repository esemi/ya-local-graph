# -*- coding: utf-8 -*-

import logging

from app.cli import graph_name, gml_name
from app.cli.graph_plot import clear_cache
from app.config import PROCESS_GENRES, ALL_ROCK_GENRE, ROCK_GENRES, ALL_METAL_GENRE, METAL_GENRES, ROCK_AND_METAL_GENRE
from app.model import fetch_graph_primary, fetch_graph_full, get_genres


def save_gml(genre_name, nodes, edges, full=False):
    logging.info('save graph %d %d', len(nodes), len(edges))

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

    def _export(genre_ids, genre_name, with_top=False):
        logging.info('export start %s %s', genre_name, genre_ids)
        nodes, edges = fetch_graph_primary(genre_ids)
        save_gml(genre_name, nodes, edges)
        nodes, edges = fetch_graph_full(genre_ids)
        save_gml(genre_name, nodes, edges, full=True)
        logging.info('end')

        if with_top:
            genre_name += '-top3'
            logging.info('export start %s %s', genre_name, genre_ids)
            nodes, edges = fetch_graph_primary(genre_ids, max_position=3)
            save_gml(genre_name, nodes, edges)
            nodes, edges = fetch_graph_full(genre_ids, max_position=3)
            save_gml(genre_name, nodes, edges, full=True)
            logging.info('end')

    logging.info('')

    for genre_name in PROCESS_GENRES:
        genre_ids = [genres[genre_name]]
        _export(genre_ids, genre_name)

    rock_ids = [str(genres[i]) for i in genres if i in ROCK_GENRES]
    metal_ids = [str(genres[i]) for i in genres if i in METAL_GENRES]
    custom_pairs = [(rock_ids, ALL_ROCK_GENRE),
                    (metal_ids, ALL_METAL_GENRE),
                    (rock_ids + metal_ids, ROCK_AND_METAL_GENRE)]
    for ids, name in custom_pairs:
        _export(ids, name, with_top=True)


if __name__ == '__main__':
    task()
