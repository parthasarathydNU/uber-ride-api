# app/models/location.py

from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4

class LocationBase(BaseModel):
    id: UUID
    name: str = Field(..., min_length=1, max_length=100, description="Name of the location")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude of the location")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude of the location")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty or just whitespace')
        return v.strip()

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):

    class Config:
        from_attributes = True

    @classmethod
    def create(cls, name: str, latitude: float, longitude: float) -> 'Location':
        """Create a new Location instance with a generated UUID."""
        return cls(id=uuid4(), name=name, latitude=latitude, longitude=longitude)

    def to_dict(self) -> dict:
        """Convert the Location object to a dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    def __eq__(self, other: object) -> bool:
        """Check if two Location objects are equal based on their ID."""
        if not isinstance(other, Location):
            return NotImplemented
        return self.id == other.id

    def __repr__(self) -> str:
        """Return a string representation of the Location object."""
        return f"Location(id={self.id}, name='{self.name}', latitude={self.latitude}, longitude={self.longitude})"
