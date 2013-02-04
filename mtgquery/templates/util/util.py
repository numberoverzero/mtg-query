import re
import markupsafe
import itertools
import urllib

def izip(*iters):
    return itertools.izip(itertools.count(), *iters)

def ifelse(condition, _if, _else):
    return _if if condition else _else

def url_escape(string):
    return urllib.quote_plus(string.encode("utf-8"))

def html_escape(string):
    return markupsafe.escape(string)

escapes = """'\""""
js_rx = re.compile('([{}])'.format(escapes))
def js_escape(string):
    return js_rx.sub(r'\\\1', string)


def pretty_print_dict(d, sep='\n'):
    return sep.join("{} : {}".format(k, d[k]) for k in d)