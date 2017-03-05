# -*- coding: utf-8 -*-

import logging
import os

from app.config import DATA_FOLDER_PATH
from app.model import fetch_graph_genre_short


def save_gml(nodes, edges, filename, directed=True):
    logging.info('save fetch genre short %d %d', len(nodes), len(edges))
    f = open(os.path.sep.join([DATA_FOLDER_PATH, filename]), 'w+')
    content = ['graph [']

    if directed:
        content.append('    directed 1')

    for id, label in nodes.items():
        content.append('    node [')
        content.append('        id %d' % id)
        content.append('        label "%s"' % label)
        content.append('    ]')

    for from_id, to_id in edges:
        content.append('    edge [')
        content.append('        source %d' % from_id)
        content.append('        target %d' % to_id)
        content.append('    ]')

    content.append(']')

    f.write("\n".join(content))
    f.close()


def task():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

    nodes, edges = fetch_graph_genre_short()
    logging.info('fetch genre short %d %d', len(nodes), len(edges))
    save_gml(nodes, edges, 'genre_short.gml')
    logging.info('graph export complete')

#         todo export only genre graph w/o single nodes
#         todo export full graph w/o single nodes


