# -*- coding: utf-8 -*-

import logging
import pickle
import os

import igraph

from app.config import ROCK_PRIMARY_FILE, ROCK_PRIMARY_PLOT_FILE, ROCK_FULL_FILE, ROCK_FULL_PLOT_FILE, METAL_FULL_FILE, \
    METAL_FULL_PLOT_FILE, METAL_PRIMARY_FILE, METAL_PRIMARY_PLOT_FILE


def cache_name(name):
    return '%s.layout' % name


def clear_cache(name):
    cache_path = cache_name(name)
    if os.path.exists(cache_path):
        os.remove(cache_path)


def read_cache(name):
    cache_path = cache_name(name)
    l = None
    try:
        with open(cache_path, 'rb') as f:
            l = pickle.load(f)
    except:
        pass
    return l


def save_cache(name, l):
    cache_path = cache_name(name)
    f = open(cache_path, 'wb')
    pickle.dump(l, f)


def plot(g, name, name_g):
    kwargs = dict(bbox=(10000, 10000), edge_arrow_size=0.3, edge_arrow_width=0.9, edge_width=0.3, vertex_frame_width=0.4)

    l = read_cache(name_g)
    if not l:
        l = g.layout('fr')
        save_cache(name_g, l)

    logging.info('compute layout')

    igraph.plot(g, name % ('label', 'svg'), vertex_size=3, vertex_label_size=7, layout=l, **kwargs)
    logging.info('plot graph base')

    g.vs['label'] = ['']
    igraph.plot(g, name % ('clear', 'png'), vertex_size=7, layout=l, **kwargs)
    igraph.plot(g, name % ('clear', 'svg'), vertex_size=7, layout=l, **kwargs)
    logging.info('plot graph w/ labels')


def task():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('start')

    g = igraph.Graph.Read_GML(METAL_PRIMARY_FILE)
    logging.info('load rock primary %d %d', g.vcount(), g.ecount())
    plot(g, METAL_PRIMARY_PLOT_FILE, METAL_PRIMARY_FILE)
    logging.info('plot end')

    g = igraph.Graph.Read_GML(ROCK_PRIMARY_FILE)
    logging.info('load rock primary %d %d', g.vcount(), g.ecount())
    plot(g, ROCK_PRIMARY_PLOT_FILE, ROCK_PRIMARY_FILE)
    logging.info('plot end')

    # g = igraph.Graph.Read_GML(METAL_FULL_FILE)
    # logging.info('load rock full %d %d', g.vcount(), g.ecount())
    # plot(g, METAL_FULL_PLOT_FILE, METAL_FULL_FILE)
    # logging.info('plot end')

    # g = igraph.Graph.Read_GML(ROCK_FULL_FILE)
    # logging.info('load rock full %d %d', g.vcount(), g.ecount())
    # plot(g, ROCK_FULL_PLOT_FILE, ROCK_FULL_FILE)
    # logging.info('plot end')



