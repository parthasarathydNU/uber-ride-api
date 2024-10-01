from typing import Union, List
from fastapi import FastAPI
from app.api.locations import router as locations_router
from app.utils.location_generator import generate_predefined_locations
from app.services.location_service import LocationService

app = FastAPI()

# Initialize locations
locations_service = LocationService(generate_predefined_locations())

# Store the service instance in the app state
app.state.locations_service = locations_service


# Include the locations router
app.include_router(locations_router, prefix="/api/v1", tags=["locations"])

@app.on_event("startup")
async def startup_event():
    print("The application is starting up...")
    print(f"Initialized with {len(app.state.locations_service.get_all_locations())} locations.")

@app.get("/")
def health_check():
    return {"Hello": "World"}

@app.on_event("shutdown")
async def shutdown_event():
    print("The application is shutting down...")
