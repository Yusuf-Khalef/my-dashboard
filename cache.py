import time

cache = {}
CACHE_SECONDS = 300

def get_cache(key):
    entry = cache.get(key)
    if entry is None:
        return None
    
    saved_time, data = entry
    if time.time() - saved_time > CACHE_SECONDS:
        return None
    return data
    
def set_cache(key, data):
    cache[key] = (time.time(), data)
    