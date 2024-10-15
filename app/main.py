# app/main.py

from fastapi import FastAPI, Depends
from app.api import locations
from app.services.location_service import LocationService
from app.utils.location_generator import generate_predefined_locations
from typing import List
from app.models.location import Location
from app.dependencies import get_location_service

app = FastAPI()



# Include routers
app.include_router(locations.router, prefix="/api/v1", tags=["locations"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)