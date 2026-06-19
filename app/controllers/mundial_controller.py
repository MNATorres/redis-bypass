import json
import redis
from fastapi import HTTPException
from app.models.cache import get_from_cache, set_in_cache, delete_from_cache
from app.models.database import consultar_base_de_datos_real, add_championship_to_db
from app.views.mundial_view import render_mundiales_response, render_invalidation_response
from app.utils.logger import logger

CACHE_KEY = "data:mundiales"

def get_mundiales():
    """
    Business coordinator to retrieve World Cup tournaments using the Cache-Aside pattern.
    """
    logger.info("Controller: Fetching championships...")
    # 1. Attempt to retrieve from Redis cache
    data_en_cache = get_from_cache(CACHE_KEY)

    if data_en_cache:
        # CACHE HIT
        try:
            parsed_data = json.loads(data_en_cache)
            logger.info("Controller: Cache hit. Rendering response from Cache.")
            return render_mundiales_response(
                source="Redis Cache (RAM)",
                data=parsed_data
            )
        except json.JSONDecodeError as e:
            # --- SELF-HEALING / AUTOMATIC CLEANUP ---
            # If data is corrupt, we proactively clean up the garbage in Redis 
            # so the next concurrent user doesn't hit the same broken string.
            logger.warning(f"Controller: Cache data is corrupt ({e}). Initializing self-healing cleanup...")
            try:
                delete_from_cache(CACHE_KEY)  # Clean up the garbage
            except Exception:
                pass  # Fault tolerance: if delete fails, don't crash the application
            
            pass  # If data is corrupt, ignore and proceed to the database
            
    # CACHE MISS
    # 2. If cache miss, query the simulated database
    logger.info("Controller: Cache miss. Directing query to simulated PostgreSQL database...")
    datos_reales = consultar_base_de_datos_real()

    # 3. Save to Redis in JSON format with an expiration of 20 seconds
    try:
        set_in_cache(CACHE_KEY, json.dumps(datos_reales), ttl_seconds=20)
    except Exception as e:
        logger.error(f"Controller: Failed to populate cache: {e}")
        pass  # Fault tolerance: do not block if Redis write fails

    logger.info("Controller: Returning database results and updating cache.")
    return render_mundiales_response(
        source="PostgreSQL Database (Hard drive)",
        data=datos_reales
    )

def invalidate_cache():
    """
    Invalidates the Redis cache to synchronize data when simulating an update.
    """
    logger.info("Controller: Manual cache invalidation triggered.")
    try:
        delete_from_cache(CACHE_KEY)
        logger.info("Controller: Cache invalidated successfully.")
        return render_invalidation_response()
    except redis.RedisError as e:
        logger.error(f"Controller: Failed to invalidate cache: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting key: {e}")

def add_championship(championship: dict):
    """
    Adds a new championship to the database and invalidates the Redis cache.
    """
    logger.info(f"Controller: Adding new championship: {championship}")
    # 1. Save new record to the database
    add_championship_to_db(championship)
    logger.info("Controller: Championship saved to mock database.")

    # 2. Invalidate cache (Delete key) to force next GET to fetch updated data
    logger.info("Controller: Invalidating cache to ensure consistency...")
    try:
        delete_from_cache(CACHE_KEY)
        logger.info("Controller: Cache invalidated after addition.")
    except Exception as e:
        logger.error(f"Controller: Cache invalidation failed: {e}")
        pass  # Fault tolerance: do not block if cache deletion fails

    # 3. Return formatted response
    return render_invalidation_response(message="Championship added successfully. Cache invalidated.")