from functools import wraps
from datetime import datetime


def time_it(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        start = datetime.now()
        print(f"[Main Process] Process start at: {start}.")
        res = func(*args, **kwargs)
        finish = datetime.now()
        print(f"[Main Process] Process start at: {start}.")
        print(f"[Main Process] Process finish at: {finish}.")
        print(f"[Main Process] Process total cost: {finish - start}.")
        return res

    return _wrapper
