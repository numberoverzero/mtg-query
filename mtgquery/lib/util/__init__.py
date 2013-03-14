##mtgquery.lib.util
import os
import errno
import itertools
import logging
import random
import time

__log = logging.getLogger(__name__)


def rel_path(file):
    '''You should always pass in __file__ from a script to get the directory it's running from.'''
    return os.path.dirname(os.path.realpath(file))


def merge_dicts(*dicts):
    '''Merges any number of dictionaries into a new dictionary'''
    return dict(itertools.chain(*[d.iteritems() for d in dicts]))


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def string_shuffle(string):
    chars = list(string)
    random.shuffle(chars)
    return ''.join(chars)


def sample_with_replacement(population, k):
    '''Uses random.choice to return a random sample of the population'''
    return (random.choice(population) for _ in xrange(k))


def simple_timer():
    '''
    Super basic function that you call when you want to start timing,
    and call again to get the delta since it started.
    '''
    start = time.time()
    return lambda: time.time() - start


def DEBUG(string):
    __log.debug(string)


def INFO(string):
    __log.info(string)


def WARN(string):
    __log.warn(string)


def ERROR(string):
    __log.error(string)


def CRITICAL(string):
    __log.critical(string)
