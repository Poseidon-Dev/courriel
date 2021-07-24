import asyncio
from typing import AnyStr

def binary_pickle(cls):
    """
    Converts a class instance into a Binary pickle for postgres storage
    """
    from pickle import dumps
    from psycopg2 import Binary
    return Binary(dumps(cls)) 

def check_domain(email):
    """
    Checks that the domain is within the list of accepted domain
    """
    from config import ACCEPTED_DOMAIN
    email = email.split('@')
    if email[1] in ACCEPTED_DOMAIN:
        return email[0].lower()
    else:
        return None

def loop(func):
    loop = asyncio.get_event_loop()
    def decorated(*args, **kwargs):
        loop.run_until_complete(func(*args, **kwargs))
    return decorated
