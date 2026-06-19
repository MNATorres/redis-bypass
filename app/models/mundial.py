from pydantic import BaseModel

class Mundial(BaseModel):
    year: int
    host: str
    winner: str
