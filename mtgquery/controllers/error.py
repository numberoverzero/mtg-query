_images = {
    '404hash': {
        'line1': u"These aren't the synergies you're looking for.",
        'line2': u"(We couldn't find the synergy hash {})",
        'img': u"404hash.png"
    },
    '404': {
        'line1': u"I have no idea what you were trying to find.",
        'line2': u"(We've alerted the proper authorities)",
        'img': u"404.png"
    },
    '403': {
        'line1': u"Nice try, pal.",
        'line2': u"(You're not authorized to view that)",
        'img': u"403.png"
    },
    '500': {
        'line1': u"Something's gone wrong.  We're.... working on it.",
        'line2': u"(Like wrenches to clockwork)",
        'img': u"500.png"
    },

}

# Use cloudinary CDN
url = u'http://res.cloudinary.com/mtg-query/image/upload/{}'
for image_dict in _images.values():
    image_dict['img'] = url.format(image_dict['img'])


def error_data(string):
    if string in _images:
        return dict(_images[string])
    return None
