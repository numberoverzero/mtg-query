from bs4 import BeautifulSoup


def add_class(text, element, *args):
    '''
    Add any number of classes to a given element type.
    Input is raw text, output is non-formatted text.
    '''

    soup = BeautifulSoup(text)
    tags = soup.findAll(element)
    for tag in tags:
        if 'class' not in tag:
            tag['class'] = []
        tag['class'].extend(args)
    string_soup = str(soup)
    return string_soup
