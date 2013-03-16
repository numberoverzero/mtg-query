from sqlalchemy.sql import func
import random
random.seed(object())


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


def get_random(session, model):
    '''
    Returns a random object from a model based on the id field.
    May take longer if rows have been deleted (will try to load non-existant rows)
    Assumes ids start at 1.
    '''
    invalid_ids = []
    max_id = session.query(func.max(model.id)).scalar()

    def generate_id():
        if len(invalid_ids) == max_id:
            return None
        while True:
            id = random.randint(1, max_id)
            if id not in invalid_ids:
                # Can only be valid once, append
                invalid_ids.append(id)
                return id

    while True:
        id = generate_id()
        if id is None:
            return None
        obj = has_model(session, model, id=id)
        if obj is not None:
            return obj
