def always_true(*args, **kwargs):
    '''Helper function for any method which takes an optional validator.'''
    return True


def noop(*args, **kwargs):
    '''Helper function that takes anything and doesn't do anything'''
    pass
