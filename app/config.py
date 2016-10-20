# -*- coding: utf-8 -*-


class DefaultConfig(object):
    DEBUG = False
    CRAWLER_USER_AGENT = 'Artist graph research'
    GRAPH_CAHCE_ENABLE = True
    GRAPH_CACHE_DIR = '/mnt/volume-fra1-02/data/source-films'


class ProductionConfig(DefaultConfig):
    pass

try:
    from config_local import DevConfig
except ImportError:
    class DevConfig(DefaultConfig):
        DEBUG = True
        SAVE_SOURCE = True
        GRAPH_CACHE_DIR = '/home/esemi/ya-graph-cache'

