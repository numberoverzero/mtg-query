import os
import logging
import itertools


def merge_dicts(*dicts):
    '''Merges any number of dictionaries into a new dictionary'''
    return dict(itertools.chain(*[d.iteritems() for d in dicts]))


def rel_path(file):
    '''You should always pass in __file__ from a script to get the directory it's running from.'''
    return os.path.dirname(os.path.realpath(file))


def get_logger(name):
    '''You should always pass in __name__ from a script to get the correct logging instance'''
    return logging.getLogger(name)
