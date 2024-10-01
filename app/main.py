# app/main.py

from fastapi import FastAPI, Depends
from app.api import locations
from app.services.location_service import LocationService
from app.utils.location_generator import generate_predefined_locations
from typing import List
from app.models.location import Location

app = FastAPI()

def get_location_service() -> LocationService:
    initial_locations: List[Location] = generate_predefined_locations()
    return LocationService(initial_locations)

@app.on_event("startup")
async def startup_event():
    app.state.location_service = get_location_service()

def get_locations_service() -> LocationService:
    return app.state.location_service

# Include routers
app.include_router(locations.router, prefix="/api/v1", tags=["locations"])

# Override for testing
def override_get_location_service() -> LocationService:
    return LocationService(initial_locations=[])  # Empty list for tests

# This will be used in tests to override the dependency
app.dependency_overrides[get_locations_service] = override_get_location_service
