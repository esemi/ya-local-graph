# -*- coding: utf-8 -*-

import logging
import pickle
import os
from copy import deepcopy

import igraph
from igraph.drawing.text import TextDrawer
import cairocffi
from PIL import Image

from app.cli import graph_path, gml_name, graph_index
from app.config import PLOT_LAYOUT, ROCK_GENRES, METAL_GENRES, ALL_METAL_GENRE, ALL_ROCK_GENRE, ROCK_AND_METAL_GENRE, \
    EXPORT_FILE_CUSTOM


PLOT_OPTIONS_PNG = {
    'rock-primary': dict(bbox=(1500, 1500), vertex_size=3, edge_arrow_size=0.2, edge_arrow_width=0.3, edge_width=0.1,
                         vertex_frame_width=0.2),

    'rock-all-primary': dict(bbox=(3000, 3000), vertex_size=3, edge_arrow_size=0.2, edge_arrow_width=0.3,
                             edge_width=0.1, vertex_frame_width=0.2),
    'rock-all-full': dict(bbox=(3000, 3000), vertex_size=3, edge_arrow_size=0.2, edge_arrow_width=0.3, edge_width=0.1,
                          vertex_frame_width=0.2),

    'metal-all-primary': dict(bbox=(3000, 3000), vertex_size=3, edge_arrow_size=0.2, edge_arrow_width=0.3,
                              edge_width=0.1, vertex_frame_width=0.2),
    'metal-all-full': dict(bbox=(3000, 3000), vertex_size=3, edge_arrow_size=0.2, edge_arrow_width=0.3, edge_width=0.1,
                           vertex_frame_width=0.2),

    'summary-full-basic': dict(bbox=(3000, 3000), vertex_size=3, edge_arrow_size=0.2, edge_arrow_width=0.3,
                               edge_width=0.1, vertex_frame_width=0.2),
    'summary-full-weight': dict(bbox=(5000, 5000), edge_arrow_size=0.1, edge_arrow_width=0.1, edge_width=0.07,
                                        vertex_frame_width=0.2),
    'summary-full-weight-big': dict(bbox=(32000, 32000), edge_arrow_size=0.15, edge_arrow_width=0.15, edge_width=0.1,
                                    vertex_frame_width=0.4, vertex_label_size=12),
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


def cache_name(name):
    return '%s.layout' % name


def plot_name(name, extension):
    return '%s.%s' % (name, extension)


def save_cache(name, l):
    f = open(cache_name(name), 'wb')
    pickle.dump(l, f)


def plot(graph, source_path, index, result_path=None, compute_closeness=True, print_label_size_min=None,
         add_legend=True, size_factor=None, bbox_size=None):
    G = deepcopy(graph)
    l = read_cache(source_path)
    if not l:
        l = G.layout(PLOT_LAYOUT)
        save_cache(source_path, l)
    logging.info('complete layout')

    if not result_path:
        result_path = source_path

    png_opt = dict(bbox=(1500, 1500), vertex_size=7, edge_arrow_size=0.2, edge_arrow_width=0.9, edge_width=0.3,
                   vertex_frame_width=0.4) if index not in PLOT_OPTIONS_PNG else PLOT_OPTIONS_PNG[index]

    if bbox_size:
        png_opt['bbox'] = (bbox_size, bbox_size)

    if print_label_size_min is None:
        G.vs['label'] = ['']
    else:
        for i in G.vs:
            try:
                if i['size'] < print_label_size_min:
                    i['label'] = ''
            except IndexError:
                pass

    if size_factor:
        m = max(G.vs['size'])
        for i in G.vs:
            try:
                i['size'] = i['size'] / m * size_factor
            except IndexError:
                pass

    p = igraph.plot(G, plot_name(result_path, 'png'), layout=l, **png_opt)
    logging.info('plot graph')
    if add_legend:
        legend = '%s: %d x %d\nclustering coef. %.4f\n' % (index, G.vcount(), G.ecount(),
                                                           G.transitivity_undirected(mode="zero"))
        if compute_closeness:
            legend += 'closeness %.4f' % (sum(G.closeness()) / G.vcount())
        logging.info('compute legend %s' % legend)
        p.redraw()
        ctx = cairocffi.Context(p.surface)
        ctx.set_font_size(40)
        # todo Use ctx.scale() for big image
        drawer = TextDrawer(ctx, legend, halign=TextDrawer.LEFT)
        drawer.draw_at(150, 50, width=500)
    p.save()
    logging.info('save png')


def task():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('start')

    def preview(index, gml_file_path, preview_size):
        preview_index = EXPORT_FILE_CUSTOM % (index, 'preview')
        im = Image.open(plot_name(gml_file_path, 'png'))
        im.thumbnail((preview_size, preview_size))
        im.save(plot_name(graph_path(preview_index), 'png'))
        logging.info('plot full preview %s' % preview_index)

    def plot_all(genre_name, full_only=False, preview_size=None):

        if not full_only:
            index = graph_index(genre_name, False)
            gml_file_path = graph_path(index)
            logging.info('start %s', index)
            graph = igraph.Graph.Read_GML(gml_name(gml_file_path))

            logging.info('loaded %d %d', graph.vcount(), graph.ecount())
            plot(graph, gml_file_path, index)
            logging.info('plot primary')

            if preview_size:
                preview(index, gml_file_path, preview_size)

        index = graph_index(genre_name, True)
        gml_file_path = graph_path(index)
        logging.info('start %s', index)
        graph = igraph.Graph.Read_GML(gml_name(gml_file_path))

        logging.info('loaded %d %d', graph.vcount(), graph.ecount())
        plot(graph, gml_file_path, index)
        logging.info('plot full')

        if preview_size:
            preview(index, gml_file_path, preview_size)

    logging.info('plot genres')
    for genre_name in (ROCK_GENRES | METAL_GENRES) - {'rock', 'metal'}:
        plot_all(genre_name, True, 350)

    logging.info('plot genres full')
    for genre_name in {ALL_ROCK_GENRE, ALL_METAL_GENRE}:
        plot_all(genre_name, preview_size=700)

    def plot_custom(source):
        index = graph_index(source, True)
        gml_file_path = graph_path(index)
        logging.info('start %s', index)
        graph = igraph.Graph.Read_GML(gml_name(gml_file_path))
        logging.info('loaded %d %d', graph.vcount(), graph.ecount())

        basic_index = EXPORT_FILE_CUSTOM % (index, 'basic')
        plot(graph, gml_file_path, basic_index, graph_path(basic_index), False)
        logging.info('plot basic')
        preview(basic_index, graph_path(basic_index), 1920)

        weight_index = EXPORT_FILE_CUSTOM % (index, 'weight')
        plot(graph, gml_file_path, weight_index, graph_path(weight_index), False, add_legend=False, size_factor=100)
        logging.info('plot w/ weight')
        preview(weight_index, graph_path(weight_index), 1920)

        for border in range(35, 15, -5):
            for size in {10, 20}:
                index_result = EXPORT_FILE_CUSTOM % (index, 'weight-%dk-%s' % (size, border))
                logging.info('plot w/ weight big %s' % index_result)
                index_props = EXPORT_FILE_CUSTOM % (index, 'weight-big')
                plot(graph, gml_file_path, index_props, graph_path(index_result), False, print_label_size_min=float(border),
                     add_legend=False, size_factor=185, bbox_size=size * 1000)

    logging.info('plot summary custom')
    plot_custom(ROCK_AND_METAL_GENRE)
