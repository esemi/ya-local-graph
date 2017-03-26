# -*- coding: utf-8 -*-

import logging
import pickle
import os

import igraph

from app.cli import cache_name, graph_name, gml_name, plot_name
from app.config import PLOT_LAYOUT, PROCESS_GENRES, ALL_METAL_GENRE, ALL_ROCK_GENRE, ROCK_AND_METAL_GENRE


def clear_cache(name):
    cache_path = cache_name(name)
    if os.path.exists(cache_path):
        os.remove(cache_path)


def read_cache(name):
    try:
        with open(cache_name(name), 'rb') as f:
            return pickle.load(f)
    except:
        return None


def save_cache(name, l):
    f = open(cache_name(name), 'wb')
    pickle.dump(l, f)


def plot(graph, name):
    l = read_cache(name)
    if not l:
        l = graph.layout(PLOT_LAYOUT)
        save_cache(name, l)
    logging.info('compute layout')

    if graph.vcount() < 500:
        size = 1000
    elif graph.vcount() < 1000:
        size = 3000
    else:
        size = 10000

    kwargs = dict(bbox=(size, size), edge_arrow_size=0.2, edge_arrow_width=0.9, edge_width=0.3, vertex_frame_width=0.4)
    igraph.plot(graph, plot_name(name, 'label', 'png'), vertex_size=3, vertex_label_size=7, layout=l, **kwargs)
    igraph.plot(graph, plot_name(name, 'label', 'svg'), vertex_size=3, vertex_label_size=7, layout=l, **kwargs)
    logging.info('plot graph w/ labels')

    graph.vs['label'] = ['']
    igraph.plot(graph, plot_name(name, 'basic', 'png'), vertex_size=7, layout=l, **kwargs)
    igraph.plot(graph, plot_name(name, 'basic', 'svg'), vertex_size=7, layout=l, **kwargs)
    logging.info('plot graph w/o labels')


def task():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('start')

    logging.info('plot primary')
    for genre_name in PROCESS_GENRES:
        name = graph_name(genre_name, False)
        logging.info('start %s', name)
        graph = igraph.Graph.Read_GML(gml_name(name))
        logging.info('loaded %d %d', graph.vcount(), graph.ecount())
        plot(graph, name)
        logging.info('plot')

    logging.info('plot full')
    for genre_name in PROCESS_GENRES:
        name = graph_name(genre_name, True)
        logging.info('start %s', name)
        graph = igraph.Graph.Read_GML(gml_name(name))
        logging.info('loaded %d %d', graph.vcount(), graph.ecount())
        plot(graph, name)
        logging.info('plot')

    name = graph_name(ALL_ROCK_GENRE, False)
    logging.info('start plot rock-all %s', name)
    graph = igraph.Graph.Read_GML(gml_name(name))
    logging.info('loaded %d %d', graph.vcount(), graph.ecount())
    plot(graph, name)
    logging.info('plot primary')

    name = graph_name(ALL_METAL_GENRE, False)
    logging.info('start plot metal-all %s', name)
    graph = igraph.Graph.Read_GML(gml_name(name))
    logging.info('loaded %d %d', graph.vcount(), graph.ecount())
    plot(graph, name)
    logging.info('plot primary')

    name = graph_name(ALL_ROCK_GENRE, True)
    logging.info('start plot rock-all %s', name)
    graph = igraph.Graph.Read_GML(gml_name(name))
    logging.info('loaded %d %d', graph.vcount(), graph.ecount())
    plot(graph, name)
    logging.info('plot full')

    name = graph_name(ALL_METAL_GENRE, True)
    logging.info('start plot metal-all %s', name)
    graph = igraph.Graph.Read_GML(gml_name(name))
    logging.info('loaded %d %d', graph.vcount(), graph.ecount())
    plot(graph, name)
    logging.info('plot full')

