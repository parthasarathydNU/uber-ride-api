from pydantic import BaseModel

class CreateLocation(BaseModel):
    name: str
    latitude: float
    longitude: float
