# This is here because when running beautifulsoup.prettify() it doesn't respect textarea whitespace,
# which really fucking sucks.  So this sentinel gets slammed onto the front and back of any text between textarea and /textarea,
# and then after we prettify the area, we chop everything between the <textarea> open and the sentinel (including the sentinel obviously)
# and we also chop everything between the second sentinel and the close textarea, also losing that sentinel.

# SUPER IMPORTANT NOTE THAT I'LL FORGET LATER: WHEN THIS NOISE GETS FIXED DONT FORGET TO DROP THIS HACK LIKE ITS HOT
# otherwise people may be all 'wtf is this horse shit in my description'
import re
from bs4 import BeautifulSoup


def bs4_hacked_prettify(string):
    ugly_string = __add_sentinel(string)
    hacked_soup = BeautifulSoup(ugly_string)
    ugly_string = hacked_soup.prettify()
    clean_string = __remove_sentinel(ugly_string)
    return clean_string

__SENTINEL__ = "something_iswrong_sendhelp"

__tas_add = re.compile(r'<textarea([^>]*)>(.*?)</textarea>', re.DOTALL)
__tas_add_replace = r'<textarea\1>{0}\2{0}</textarea>'.format(__SENTINEL__)

__tas_remove = re.compile(r'<textarea([^>]*)>(\s*{0})(.*?)({0}\s*)</textarea>'.format(__SENTINEL__), re.DOTALL)
__tas_remove_replace = r'<textarea\1>\3</textarea>'

__code_add = re.compile(r'<code([^>]*)>(.*?)</code>', re.DOTALL)
__code_add_replace = r'<code\1>{0}\2{0}</code>'.format(__SENTINEL__)

__code_remove = re.compile(r'<pre([^>]*)>(\s*)<code([^>]*)>(\s*{0})(.*?)({0}\s*)</code>(\s*)</pre>'.format(__SENTINEL__), re.DOTALL)
__code_remove_replace = r'<pre\1><code\3>\5</code></pre>'


def __remove_sentinel(string):
    if string is None:
        return string
    string = __tas_remove.sub(__tas_remove_replace, string)
    string = __code_remove.sub(__code_remove_replace, string)
    return string


def __add_sentinel(string):
    if string is None:
        return string
    string = __tas_add.sub(__tas_add_replace, string)
    string = __code_add.sub(__code_add_replace, string)
    return string

if __name__ == "__main__":
    add_tests = [
        ('hello!', 'hello!'),
        ('textarea', 'textarea'),
        ('<textarea></textarea>', '<textarea>{0}{0}</textarea>'.format(__SENTINEL__)),
        ('<textarea>Hello!</textarea>', '<textarea>{0}Hello!{0}</textarea>'.format(__SENTINEL__)),
        ('<textarea>\nHello!\n</textarea>', '<textarea>{0}\nHello!\n{0}</textarea>'.format(__SENTINEL__))
    ]
    remove_tests = [(e, s) for (s, e) in add_tests]
    runs = [
        ("Add", __add_sentinel, add_tests),
        ("Remove", __remove_sentinel, remove_tests),
    ]

    for label, func, tests in runs:
        print label + " Tests"
        for i, (string, expected) in enumerate(tests):
            actual = func(string)
            if expected != actual:
                print label + " FAILED: INPUT |{}| EXPECTED |{}| OUTPUT |{}|".format(
                                        string, expected, actual)
            else:
                print "Test {} passed".format(i)
