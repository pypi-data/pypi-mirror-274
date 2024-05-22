import time
from contextlib import contextmanager

import pandas as pd


def timer(func):

    def wrapper(*args, **kwargs):
        s = time.time()
        result = func(*args, **kwargs)
        e = time.time() - s
        print(f'[{func.__name__}] {e:.2f}s')

        return result

    return wrapper


@contextmanager
def time_block(task_name: str):
    s = time.time()
    yield
    e = time.time() - s
    print(f"[{task_name}] {e:.2f}s")


def as_df(func) -> pd.DataFrame:
    '''Decorator to convert func output into a pd.DataFrame if output is 
    iterable.'''

    def wrapper(*args, **kwargs):
        objs = func(*args, **kwargs)
        if hasattr(objs, '__iter__'):
            return pd.DataFrame(objs)
        else:
            return objs

    return wrapper
