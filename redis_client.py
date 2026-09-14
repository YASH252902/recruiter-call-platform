import redis
import os

REDIS_ENABLED = os.getenv("REDIS_ENABLED", "true").lower() == "true"

if REDIS_ENABLED:
    try:
        r = redis.Redis(host="redis", port=6379, decode_responses=True, socket_connect_timeout=2)
        r.ping()
    except Exception:
        r = None
else:
    r = None

def get_cached_value(key: str):
    if not r:
        return None
    try:
        return r.get(key)
    except Exception:
        return None

def set_cached_value(key: str, value: str, expire_seconds: int = 60):
    if not r:
        return
    try:
        r.set(key, value, ex=expire_seconds)
    except Exception:
        pass