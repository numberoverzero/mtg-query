##mtgquery.lib.notifications
__notifications = {}

def register_notification(notification_cls, name):
    __notifications[name] = notification_cls

def load_class(name):
    return __notifications.get(name, None)

def to_string(notification):
    return notification.to_flash_string()

def from_string(notification_string):
    '''returns the object version of a notification string, or None'''
    if notification_string is None or len(notification_string) == 0:
        return None
    
    pieces = notification_string.split(':')
    if len(pieces) < 2:
        return None

    name = pieces[0]
    notification_cls = load_class(name)
    if notification_cls is None: return None

    return notification_cls.load_from(notification_string)

def load_from_flash(session, queue=''):
    strings = session.pop_flash(queue)
    return [from_string(s) for s in strings]

def enqueue(notification, session, queue=''):
    session.flash(to_string(notification), queue)

from notification import *

ntypes = [
    GenericNotification,
    InvalidLine,
    UnknownCardName,
    UnknownSetName,
    InvalidSet,
]

for ntype in ntypes:
    register_notification(ntype, ntype.notification_name)