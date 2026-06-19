import time
from typing import List, Dict, Any

_DATABASE_MOCK = [
    {"year": 2022, "host": "Qatar", "winner": "Argentina"},
    {"year": 2018, "host": "Russia", "winner": "France"},
    {"year": 2014, "host": "Brazil", "winner": "Germany"}
]

def consultar_base_de_datos_real() -> List[Dict[str, Any]]:
    """
    Simulates a complex JOIN or a heavy query hitting the hard disk.
    Intentionally sleeps for 3 seconds to demonstrate physical latency.
    """
    time.sleep(3.0) 
    return list(_DATABASE_MOCK)

def add_championship_to_db(championship: Dict[str, Any]) -> None:
    """
    Simulates inserting a new championship record into the database.
    """
    _DATABASE_MOCK.append(championship)

