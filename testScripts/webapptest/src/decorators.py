from threading import Thread
from functools import wraps


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper

def storeresult(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            args[0].doc['result'] = 1
            return f(*args, **kwargs)
        except Exception as e: #AssertionError #ElementClickInterceptedException
            args[0].doc['result'] = 0
            raise

    return wrapper