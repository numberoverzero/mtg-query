import os


def rel_path(file):
    '''You should always pass in __file__ from a script to get the directory it's running from.'''
    return os.path.dirname(os.path.realpath(file))
