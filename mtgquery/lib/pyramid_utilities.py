def load_from_flash(session, queue_name=''):
    return session.pop_flash(queue_name)


def enqueue(string, session, queue_name=''):
    session.flash(unicode(string), queue_name)
