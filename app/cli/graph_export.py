# -*- coding: utf-8 -*-

import logging

from app.cli import graph_path, gml_name, graph_index
from app.cli.graph_plot import clear_cache
from app.config import PROCESS_GENRES, TOP3_POSTFIX, ALL_ROCK_GENRE, ROCK_GENRES, ALL_METAL_GENRE, METAL_GENRES, \
    ROCK_AND_METAL_GENRE, TOP6_POSTFIX
from app.model import fetch_graph_primary, fetch_graph_full, get_genres, fetch_graph_custom


def save_gml(genre_name, nodes, edges, full=False):
    logging.info('save graph %d %d', len(nodes), len(edges))

    g_name = graph_path(graph_index(genre_name, full))
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
    rock_ids = [str(genres[i]) for i in genres if i in ROCK_GENRES]
    metal_ids = [str(genres[i]) for i in genres if i in METAL_GENRES]

    def _export(genre_ids, genre_name):
        logging.info('export start %s %s', genre_name, genre_ids)
        nodes, edges = fetch_graph_primary(genre_ids)
        save_gml(genre_name, nodes, edges)
        nodes, edges = fetch_graph_full(genre_ids)
        save_gml(genre_name, nodes, edges, full=True)
        logging.info('end')

    logging.info('')

    for genre_name in PROCESS_GENRES:
        genre_ids = [genres[genre_name]]
        _export(genre_ids, genre_name)

    custom_pairs = [(rock_ids, ALL_ROCK_GENRE),
                    (metal_ids, ALL_METAL_GENRE)]
    for ids, name in custom_pairs:
        _export(ids, name)

    # custom export colorized graph
    logging.info('export customs primary start %s %s', ROCK_AND_METAL_GENRE, rock_ids + metal_ids)
    nodes, edges = fetch_graph_custom(rock_ids, metal_ids)
    save_gml(ROCK_AND_METAL_GENRE, nodes, edges)
    nodes, edges = fetch_graph_custom(rock_ids, metal_ids, 6)
    save_gml(ROCK_AND_METAL_GENRE + TOP6_POSTFIX, nodes, edges)
    nodes, edges = fetch_graph_custom(rock_ids, metal_ids, 3)
    save_gml(ROCK_AND_METAL_GENRE + TOP3_POSTFIX, nodes, edges)

    logging.info('export customs full start %s %s', ROCK_AND_METAL_GENRE, rock_ids + metal_ids)
    nodes, edges = fetch_graph_custom(rock_ids, metal_ids, primary=False)
    save_gml(ROCK_AND_METAL_GENRE, nodes, edges, full=True)
    nodes, edges = fetch_graph_custom(rock_ids, metal_ids, 6, primary=False)
    save_gml(ROCK_AND_METAL_GENRE + TOP6_POSTFIX, nodes, edges, full=True)
    nodes, edges = fetch_graph_custom(rock_ids, metal_ids, 3, primary=False)
    save_gml(ROCK_AND_METAL_GENRE + TOP3_POSTFIX, nodes, edges, full=True)
    logging.info('end')


if __name__ == '__main__':
    task()
