from django.utils import timezone
from django.db import connection, reset_queries
import time
from main.settings import cache
def debugger(func):
    def wrapper(*args, **kwargs):
        reset_queries()
        st = time.time()
        value = func(*args, **kwargs)
        et = time.time()
        queries = len(connection.queries)
        cache.incrby('count', 1)
        count = cache.get('count')
        # print(count)
        print(f'\n----------\nconnetion number: {queries}\ntaketime= {(et - st):.3f}\n----------')
        return value
    return wrapper