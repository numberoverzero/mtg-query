import random
from ..lib.util import string_shuffle

__b58chars = 'abcdefghijkmnopqrstuvwxyz123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
__b58chars = string_shuffle(__b58chars)

__b58base = len(__b58chars)

__HARD_MAX = 10000
__HARD_MIN = 1

def encode(value):
    encoded = ''
    while value >= 58:
        div, mod = divmod(value, 58)
        encoded = __b58chars[mod] + encoded # add to left
        value = div
    encoded = __b58chars[value] + encoded # most significant remainder
    return encoded

def decode(encoded):
    value = 0
    column_multiplier = 1;
    for c in encoded[::-1]:
        column = __b58chars.index(c)
        value += column * column_multiplier
        column_multiplier *= 58
    return value

def from_seq_with_rand(seq, rand, seq_len = 6, rand_len = 6):
    '''
    Pulls a random number with rand_len digits from rand,
    then concatenates that with seq, formatted for seq_len.
    Example:
        seq = 123
        seq_len = 6
        rand_len = 4

        computed_random = rand.randint(1000, 9999) = 4531
        computed_int = 4531000123
        return encode(4531000123)
    '''
    random_value = rand.randint(10**(rand_len-1), 10**rand_len-1)
    as_str = "{r}{seq:0{w}d}".format(r=random_value, seq=seq, w=seq_len)
    computed_int = int(as_str)
    return encode(computed_int)

def get_seq_from(hash, seq_len, rand_len):
    '''
    Returns the sequential id from a given hash
    '''
    computed_int = str(decode(hash))
    return int(computed_int[rand_len:])

def gen_random(exact_length=None, min_length=None,
               max_length=None, validate=None):
    '''
    validate should be a function that takes an (int, string) tuple of (generating int, generated hash)
        and returns an int:
            Positive if the generated value is acceptable
            Negative if the generated value is not acceptable and we should keep trying to find new values
            0 if we should stop trying to generate a hash and just return None
    specified lengths are of th resulting hash, not the integer used to generate the hash.

    if validate is None, the first generated value will always be accepted.

    must specify at least one of min/max/exact length.
        If only min/max is specified and not the other,
        the other limit is 10000, 0 respectively

    if exact length is specified, this overrides any min/max specified.

    since this uses random.randint(computed_min, computed_max) as a generation method, it will never
        stop trying numbers, even when it has tried every possibility between min, max.  It is up to
        the validate function to keep track of trials and bail when there is no acceptable value.
    returns an (int, string) tuple of (generating integer, generated hash) or None if the validate breaks the loop.
    '''
            
    if exact_length is None and min_length is None and max_length is None:
        raise ValueError('No guidance given on length')

    if validate is None:
        validate = lambda _: 1

    #Define lower limit
    if min_length is not None:
        cmin_length = min_length
    else:
        cmin_length = __HARD_MIN

    #Define upper limit
    if max_length is not None:
        cmax_length = max_length
    else:
        cmax_length = __HARD_MAX

    #Use exact
    if exact_length is not None:
        cmin_length = exact_length
        cmax_length = exact_length

    #Safe check on invalid lengths
    if cmin_length < 1: cmin_length = 1
    if cmax_length < 1: cmax_length = 1
    
    #Convert min/max hash lengths to min/max int values
    computed_min = 1 + __b58base ** (cmin_length - 1)
    computed_max = __b58base ** cmax_length

    valid = -1
    while True:
        generating_int = random.randint(computed_min, computed_max)
        generated_hash = encode(generating_int)
        result = (generating_int, generated_hash)
        valid = validate(result)
        if valid > 0:
            return result
        elif valid == 0:
            return None
        else:
            #Keep trying
            pass
