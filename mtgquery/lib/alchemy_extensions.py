from sqlalchemy.orm import subqueryload
from sqlalchemy.sql import func
import random


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
    (Really just an alias to query)
    '''
    return session.query(model).filter_by(**kwargs).first()


def get_random(session, model, field='id'):
    '''
    Returns a random object from a model based on the given field.
    The field must have positive itegral values (id is the usual culprit here)
    May take longer if rows have been deleted (will try to load non-existant rows)
    '''
    bad_vals = []
    max_val = session.query(func.max(getattr(model, field))).scalar()

    def values():
        if len(bad_vals) == max_val:
            yield None
        while True:
            val = random.randint(1, max_val)
            if val not in bad_vals:
                # Can only be valid once, append
                bad_vals.append(val)
                yield val

    for value in values():
        if value is None:
            return None
        obj = has_model(session, model, **{field: value})
        if obj is not None:
            return obj


def get_last_n(session, model, n, field='id', subquery_fields=None):
    '''
    Returns the last n objects in the table,
    by id.  If there are less than n objects,
    returns as many as possible
    '''
    field = getattr(model, field).desc()
    query = session.query(model).order_by(field)
    if subquery_fields:
        for sq_field in subquery_fields:
            field = getattr(model, sq_field)
            query = query.options(subqueryload(field))
    r = query.limit(n)
    return r
