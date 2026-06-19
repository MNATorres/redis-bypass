import json
import redis
from fastapi import HTTPException
from app.models.cache import get_from_cache, set_in_cache, delete_from_cache
from app.models.database import consultar_base_de_datos_real
from app.views.mundial_view import render_mundiales_response, render_invalidation_response

CACHE_KEY = "data:mundiales"

def get_mundiales():
    """
    Business coordinator to retrieve World Cup tournaments using the Cache-Aside pattern.
    """
    # 1. Attempt to retrieve from Redis cache
    data_en_cache = get_from_cache(CACHE_KEY)

    if data_en_cache:
        # CACHE HIT
        try:
            parsed_data = json.loads(data_en_cache)
            return render_mundiales_response(
                source="Redis Cache (RAM)",
                data=parsed_data
            )
        except json.JSONDecodeError:
            pass  # If data is corrupt, ignore and proceed to the database

    # CACHE MISS
    # 2. If cache miss, query the simulated database
    datos_reales = consultar_base_de_datos_real()

    # 3. Save to Redis in JSON format with an expiration of 20 seconds
    try:
        set_in_cache(CACHE_KEY, json.dumps(datos_reales), ttl_seconds=20)
    except Exception:
        pass  # Fault tolerance: do not block if Redis write fails

    return render_mundiales_response(
        source="PostgreSQL Database (Hard drive)",
        data=datos_reales
    )

def invalidate_cache():
    """
    Invalidates the Redis cache to synchronize data when simulating an update.
    """
    try:
        delete_from_cache(CACHE_KEY)
        return render_invalidation_response()
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Error deleting key: {e}")
