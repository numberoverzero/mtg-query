def get_or_create(session, model, **kwargs):
    '''
    Gets an object if it exists, otherwise returns a new model.
    Useful since SQLAlchemy's "unique=True" Column constraint doesn't do what you'd think it does.
    '''
    instance = has_model(session, model, **kwargs)
    return instance if instance else model(**kwargs)


def has_model(session, model, **kwargs):
    '''
    Returns an object if it exists, or None if it doesn't.
    (Really just an alias to the first function)
    '''
    return session.query(model).filter_by(**kwargs).first()
