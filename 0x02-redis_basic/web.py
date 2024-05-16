#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''The module-level Redis instance.
'''


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        # Get the current count before the request
        current_count = int(redis_store.get(f'count:{url}').decode('utf-8') or 0)
        redis_store.incr(f'count:{url}', current_count)  # Increment from previous count

        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)  # Reset to 0 after successful fetch
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text

# Test the code
print(get_page("https://example.com"))  # This will call and cache the request
print(redis_store.get(f'count:https://example.com').decode('utf-8'))  # Expected output: 1
