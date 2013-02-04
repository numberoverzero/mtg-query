from common_func import always_true
def rate_limit(gen, limit, validating_func=None, on_limit=None):
    '''
    gen is the generator to wrap.  this function will yield values from that generator
    until either that generator stops yielding values, or the limit on valid yields is hit.

    limit is the maximum number of valid values to return from the wrapped generator.
        NOTE that the generating function will stop being called once the number of valid invocations == limit

    validating_func is an optional function that inspects the return values from the generator,
        and returns true if the generator's output should be counted against the maximum.
        This is useful when parsing string input line by line, and you don't want to count empty
        lines against the limit (or you don't want to count returns of None against a limit).

        If no function is provided, every item from the generator is counted against the limit,
        including None and other falsey values.

    on_limit is an optional function that takes the (iteration_index, limit, last_value) tuple
        where iteration_index is an integer representing the number of calls to the generator,
            regardless of whether the value was valid.
            limit is the limit passed in, and last_value is the last value returned from the generator.
    '''

    if validating_func is None: 
        validating_func = always_true
    if on_limit is None:
        on_limit = always_true

    valid_returns = 0
    for i, value in enumerate(gen):
        valid = validating_func(value)
        if valid: valid_returns += 1
        if valid_returns > limit:
            on_limit((i, limit, value))
            break
        yield value

def line_generator(string, ignore_empty_lines=False):
    '''Splits a string on '\n'.  If ignore_empty_lines, does not return strings that are all whitespace characters.'''
    #Convert windows line ends
    string = string.replace("\r\n", "\n")
    for line in string.split('\n'):
        if ignore_empty_lines and len(line.strip()) == 0:
            #The line is nothing but whitespace and we're supposed to skip that
            continue
        yield line