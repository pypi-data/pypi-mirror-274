from datetime import date
from urllib.parse import quote


def encode_parameters(*args):
    for arg in args:
        if isinstance(arg, str):
            yield quote(arg)
        elif isinstance(arg, date):
            yield quote(arg.strftime("%Y-%m-%d"))
    return [quote(arg) for arg in args]
