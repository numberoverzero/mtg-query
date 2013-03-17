from bs4 import BeautifulSoup


def add_class(text, element, *classes):
    '''
    Add any number of classes to a given element type.
    Input is raw text, output is non-formatted text.
    '''

    soup = BeautifulSoup(text)
    tags = soup.findAll(element)
    for tag in tags:
        if 'class' not in tag:
            tag['class'] = []
        tag['class'].extend(classes)
    string_soup = unicode(soup)
    return string_soup
