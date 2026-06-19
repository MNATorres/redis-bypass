from typing import Dict

def check_health() -> Dict[str, str]:
    """
    Controller to return the current health status of the microservice infrastructure.
    """
    return {"status": "ok", "infrastructure": "stable"}
