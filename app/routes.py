from fastapi import APIRouter
from app.controllers import mundial_controller, health_controller
from app.models.mundial import Mundial

router = APIRouter()

@router.get("/api/v1/mundiales", tags=["Mundiales"])
def get_mundiales():
    """
    Retrieves the list of the latest World Cup tournaments.
    Applies caching (Cache-Aside) and delegates to the controller.
    """
    return mundial_controller.get_mundiales()

@router.post("/api/v1/mundiales/invalidar", tags=["Mundiales"])
def force_invalidation():
    """
    Manually invalidates the cache for the World Cup tournaments.
    """
    return mundial_controller.invalidate_cache()

@router.post("/api/v1/mundiales/add_championship", tags=["Mundiales"])
def add_championship(championship: Mundial):
    """
    Adds a new World Cup championship.
    """
    return mundial_controller.add_championship(championship.model_dump())

@router.get("/health", tags=["System"])
def health_check():
    """
    Verifies the general status and health of the application.
    """
    return health_controller.check_health()
