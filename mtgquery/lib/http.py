import xml.etree.ElementTree
import eventlet
from eventlet.green import urllib2
pool = eventlet.GreenPool()


def get_html(url):
    """Blocking call, use get_htmls for batch gets"""
    return urllib2.urlopen(url).read()


def get_htmls(urls):
    return pool.imap(get_html, urls)


def get_xml(html):
    """Converts html responses"""
    return xml.etree.ElementTree.fromstring(html)


def uri_encode(string):
    """Escapes everything"""
    return urllib2.quote(string, '')
