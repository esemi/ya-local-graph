#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import importlib


if __name__ == '__main__':
    try:
        full_name = 'app.cli.%s' % sys.argv[1]
        m = importlib.import_module(full_name)
        m.task(*sys.argv[2:])
    except IndexError:
        raise Exception('Select task name')
    except ImportError:
        raise Exception('Not found task')

