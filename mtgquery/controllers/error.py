_images = {
    '404hash': {
        'line1': "These aren't the synergies you're looking for.",
        'line2': "(We couldn't find the synergy hash {})",
        'img': "404hash.png"
    },
    '404': {
        'line1': "I have no idea what you were trying to find.",
        'line2': "(We've alerted the proper authorities)",
        'img': "404.png"
    },
    '403': {
        'line1': "Nice try, pal.",
        'line2': "(You're not authorized to view that)",
        'img': "403.png"
    },
    '500': {
        'line1': "Something's gone wrong.  We're.... working on it.",
        'line2': "(Like wrenches to clockwork)",
        'img': "500.png"
    },

}

# Use cloudinary CDN
url = 'http://res.cloudinary.com/mtg-query/image/upload/{}'
for image_dict in _images.values():
    image_dict['img'] = url.format(image_dict['img'])


def error_data(string):
    if string in _images:
        return dict(_images[string])
    return None
