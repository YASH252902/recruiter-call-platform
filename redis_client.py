import redis

r = redis.Redis(host="redis", port=6379, decode_responses=True)

def get_cached_value(key: str):
    return r.get(key)

def set_cached_value(key: str, value: str, expire_seconds: int = 60):
    r.set(key, value, ex=expire_seconds)