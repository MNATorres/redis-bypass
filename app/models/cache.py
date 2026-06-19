import redis
from typing import Optional

# Connection to the isolated Redis container (standard port 6379)
# decode_responses=True automatically decodes Redis bytes to Python strings
try:
    redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
except Exception as e:
    print(f"Error initializing Redis client: {e}")
    redis_client = None

def get_from_cache(key: str) -> Optional[str]:
    """
    Attempts to retrieve a value from the Redis cache.
    If Redis is unavailable or fails, it gracefully returns None.
    """
    if redis_client is None:
        return None
    try:
        value = redis_client.get(key)
        if isinstance(value, bytes):
            return value.decode("utf-8")
        return value
    except redis.RedisError as e:
        print(f"Error reading from Redis: {e}")
        return None

def set_in_cache(key: str, value: str, ttl_seconds: int = 20) -> bool:
    """
    Saves a value in the Redis cache with a TTL (Time To Live).
    Tolerates connection failures.
    """
    if redis_client is None:
        return False
    try:
        redis_client.setex(name=key, time=ttl_seconds, value=value)
        return True
    except redis.RedisError as e:
        print(f"Error writing to Redis: {e}")
        return False

def delete_from_cache(key: str) -> bool:
    """
    Deletes a key from the Redis cache.
    Propagates Redis exceptions so they can be handled in higher levels if needed.
    """
    if redis_client is None:
        raise redis.RedisError("The Redis client is not connected or initialized.")
    redis_client.delete(key)
    return True
