from markupsafe import escape as h

on_ready_str = u"""$(document).ready(function(){{\n{s}\n}});"""
class Page(object):
    def __init__(self):
        self.css = set()
        self.js = []
        self.js_ready = []
    
    def css_link(self, path, media = ''):
        path = h(path)
        css = """<link rel="stylesheet" type="text/css" href="{}" media="{}"></link>""".format(path, media)
        self.css.add(css)
        return ''
    
    def js_script(self, path):
        js = """<script src="{}"></script>""".format(path)
        self.js.append(js)
        return ''
    
    def on_ready(self, script):
        self.js_ready.append(script)
        return ''

    def render_css(self):
        return '\n'.join(self.css)

    def render_js(self):
        return '\n'.join(self.js)

    def render_on_ready(self):
        js_ready = '\n'.join(self.js_ready)
        return on_ready_str.format(js_ready)