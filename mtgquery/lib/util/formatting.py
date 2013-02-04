
def fmt_iter(iterable, surrounding="()", sep=", ", quote_items = False, str_func = str):
    return "{open}{items}{close}".format(
         open=surrounding[0],
         close=surrounding[1],
         items=sep.join( map(str_func, iterable) )
         )

def DEBUG(value):
    return "="*30 + "\n" + str(value) + "\n" + "="*30