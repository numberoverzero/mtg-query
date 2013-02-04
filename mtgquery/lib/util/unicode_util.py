# -*- coding: utf-8 -*-
replacements = [
    (u'&AElig;', u'Æ')
]


class AutomagicUnicode(object):
    '''
    Temporarily replaces whitelisted unicode characters with ascii placeholders.
    Once the context closes, placeholders are swapped for their appropriate unicode values.
    '''
    def __init__(self, string):
        if isinstance(string, unicode):
            self.str = string
        else:
            self.str = unicode(string, encoding="utf-8")

    def __enter__(self):
        self._to_ascii()

    def __exit__(self, type, value, tb):
        self._to_unicode()

    def _to_ascii(self):
        for ascii, uni in replacements:
            self.str = self.str.replace(uni, ascii)

    def _to_unicode(self):
        if not isinstance(self.str, unicode):
            self.str = unicode(self.str, encoding="utf-8")
        for ascii, uni in replacements:
            self.str = self.str.replace(ascii, uni)
