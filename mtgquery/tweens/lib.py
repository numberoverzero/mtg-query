
#Pages we don't want to do anything clever with
skip_exts = [
    'js',
    'css',
    'jpg',
    'png'
]

def skip_page(url):
    if url is None: return True
    return any('.'+ext in url for ext in skip_exts)