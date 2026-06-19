from typing import List, Dict, Any

def render_mundiales_response(source: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Formats the response for the World Cups listing, specifying the data source.
    """
    return {
        "source": source,
        "data": data
    }

def render_invalidation_response(message: str = "Cache successfully invalidated. Next read will query the database.") -> Dict[str, Any]:
    """
    Formats the success response for cache invalidation.
    """
    return {
        "status": "success",
        "message": message
    }
