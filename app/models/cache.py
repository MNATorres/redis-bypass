import redis
from typing import Optional
from app.utils.logger import logger

# Connection to the isolated Redis container (standard port 6379)
# decode_responses=True automatically decodes Redis bytes to Python strings
try:
    logger.info("Initializing Redis client connection to 127.0.0.1:6379...")
    redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
except Exception as e:
    logger.error(f"Error initializing Redis client: {e}")
    redis_client = None

def get_from_cache(key: str) -> Optional[str]:
    """
    Attempts to retrieve a value from the Redis cache.
    If Redis is unavailable or fails, it gracefully returns None.
    """
    if redis_client is None:
        logger.warning(f"Redis GET bypassed: Redis client is not initialized for key '{key}'")
        return None
    try:
        logger.info(f"Redis GET: Querying key '{key}'")
        value = redis_client.get(key)
        if value is not None:
            logger.info(f"Redis CACHE HIT: Key '{key}' found")
        else:
            logger.info(f"Redis CACHE MISS: Key '{key}' not found")
        
        if isinstance(value, bytes):
            return value.decode("utf-8")
        return value
    except redis.RedisError as e:
        logger.error(f"Error reading from Redis key '{key}': {e}")
        return None

def set_in_cache(key: str, value: str, ttl_seconds: int = 20) -> bool:
    """
    Saves a value in the Redis cache with a TTL (Time To Live).
    Tolerates connection failures.
    """
    if redis_client is None:
        logger.warning(f"Redis SET bypassed: Redis client is not initialized for key '{key}'")
        return False
    try:
        logger.info(f"Redis SET: Storing key '{key}' with TTL {ttl_seconds} seconds")
        redis_client.setex(name=key, time=ttl_seconds, value=value)
        logger.info(f"Redis SET Success: Key '{key}' stored successfully")
        return True
    except redis.RedisError as e:
        logger.error(f"Error writing to Redis key '{key}': {e}")
        return False

def delete_from_cache(key: str) -> bool:
    """
    Deletes a key from the Redis cache.
    Propagates Redis exceptions so they can be handled in higher levels if needed.
    """
    if redis_client is None:
        logger.error(f"Redis DEL Failed: Redis client is not connected for key '{key}'")
        raise redis.RedisError("The Redis client is not connected or initialized.")
    try:
        logger.info(f"Redis DEL: Deleting key '{key}'")
        redis_client.delete(key)
        logger.info(f"Redis DEL Success: Key '{key}' deleted successfully")
        return True
    except redis.RedisError as e:
        logger.error(f"Error deleting key '{key}' from Redis: {e}")
        raise
