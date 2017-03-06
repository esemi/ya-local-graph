# -*- coding: utf-8 -*-

import logging

import igraph

from app.config import SHORT_GRAPH_FILE, SHORT_GRAPH_PLOT_FILE, FULL_GRAPH_FILE, FULL_GRAPH_PLOT_FILE


def plot(g, name):
    kwargs = dict(bbox=(10000, 10000), edge_arrow_size=0.2, edge_arrow_width=0.8, edge_width=0.1)

    l = g.layout('fr')
    logging.info('compute layout')

    igraph.plot(g, name % '1', vertex_shape='hidden', vertex_label_size=5, layout=l, **kwargs)
    logging.info('plot graph base')

    g.vs['label'] = ['']
    igraph.plot(g, name % 2, vertex_size=5, vertex_frame_width=0.1, layout=l, **kwargs)
    logging.info('plot graph w/ labels')


def task():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('start')

    g = igraph.Graph.Read_GML(SHORT_GRAPH_FILE)
    logging.info('load short %d %d', g.vcount(), g.ecount())
    plot(g, SHORT_GRAPH_PLOT_FILE)
    logging.info('plot short')

    g = igraph.Graph.Read_GML(FULL_GRAPH_FILE)
    logging.info('load full %d %d', g.vcount(), g.ecount())
    plot(g, FULL_GRAPH_PLOT_FILE)
    logging.info('plot full')


