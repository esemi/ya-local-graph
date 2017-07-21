# -*- coding: utf-8 -*-

import logging
import pickle
import os

import igraph
from igraph.drawing.text import TextDrawer
import cairocffi

from app.cli import cache_name, graph_path, gml_name, plot_name, graph_index
from app.config import PLOT_LAYOUT, PROCESS_GENRES, ALL_METAL_GENRE, ALL_ROCK_GENRE, ROCK_AND_METAL_GENRE, TOP_POSTFIX


PLOT_OPTIONS_PNG = {
    'rock-primary': dict(bbox=(1500, 1500), vertex_size=3, edge_arrow_size=0.2, edge_arrow_width=0.3, edge_width=0.1,
                         vertex_frame_width=0.2),
    'rock-all-primary': dict(bbox=(3000, 3000), vertex_size=3, edge_arrow_size=0.2, edge_arrow_width=0.3,
                             edge_width=0.1, vertex_frame_width=0.2),
    'rock-all-full': dict(bbox=(3000, 3000), vertex_size=3, edge_arrow_size=0.2, edge_arrow_width=0.3,
                          edge_width=0.1, vertex_frame_width=0.2),
}

PLOT_OPTIONS_SVG = {
    'rock-primary': dict(bbox=(5000, 5000), vertex_size=2, vertex_label_size=3, edge_arrow_size=0.15,
                         edge_arrow_width=0.3, edge_width=0.15, vertex_frame_width=0.2),
    'rock-all-primary': dict(bbox=(5000, 5000), vertex_size=2, vertex_label_size=3, edge_arrow_size=0.15,
                             edge_arrow_width=0.3, edge_width=0.15, vertex_frame_width=0.2),
    'rock-all-full': dict(bbox=(5000, 5000), vertex_size=2, vertex_label_size=3, edge_arrow_size=0.15,
                          edge_arrow_width=0.3, edge_width=0.15, vertex_frame_width=0.2),

}


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


def plot(graph, name, index):
    l = read_cache(name)
    if not l:
        l = graph.layout(PLOT_LAYOUT)
        save_cache(name, l)
    logging.info('complete layout')

    png_opt = dict(bbox=(1500, 1500), vertex_size=7, edge_arrow_size=0.2, edge_arrow_width=0.9, edge_width=0.3,
                   vertex_frame_width=0.4) if index not in PLOT_OPTIONS_PNG else PLOT_OPTIONS_PNG[index]
    svg_opt = dict(bbox=(3000, 3000), vertex_size=3, vertex_label_size=7, edge_arrow_size=0.15,
                   edge_arrow_width=0.7, edge_width=0.2, vertex_frame_width=0.3) if index not in PLOT_OPTIONS_SVG else PLOT_OPTIONS_SVG[index]

    igraph.plot(graph, plot_name(name, 'svg'), layout=l, **svg_opt)

    graph.vs['label'] = ['']
    plot = igraph.plot(graph, plot_name(name, 'png'), layout=l, **png_opt)
    legend = '%s: %d x %d' % (index, graph.vcount(), graph.ecount())
    plot.redraw()
    ctx = cairocffi.Context(plot.surface)
    ctx.set_font_size(36)
    drawer = TextDrawer(ctx, legend, halign=TextDrawer.CENTER)
    drawer.draw_at(150, 50, width=500)
    plot.save()


def task():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('start')

    def _plot_all(genre_name):
        name = graph_path(graph_index(genre_name, False))
        logging.info('start %s', graph_index(genre_name, False))
        graph = igraph.Graph.Read_GML(gml_name(name))
        logging.info('loaded %d %d', graph.vcount(), graph.ecount())
        plot(graph, name, graph_index(genre_name, False))
        logging.info('plot primary')

        name = graph_path(graph_index(genre_name, True))
        logging.info('start %s', graph_index(genre_name, True))
        graph = igraph.Graph.Read_GML(gml_name(name))
        logging.info('loaded %d %d', graph.vcount(), graph.ecount())
        plot(graph, name, graph_index(genre_name, True))
        logging.info('plot full')

    logging.info('plot basic')
    for genre_name in PROCESS_GENRES - {'rock', 'metal'} | {ALL_ROCK_GENRE, ALL_METAL_GENRE}:
        _plot_all(genre_name)

    logging.info('plot custom')
    _plot_all(ROCK_AND_METAL_GENRE)
    _plot_all(ROCK_AND_METAL_GENRE + TOP_POSTFIX)
