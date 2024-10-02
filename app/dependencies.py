# app/dependencies.py

from fastapi import Request
from app.utils.location_generator import generate_predefined_locations
from app.services.location_service import LocationService

def get_location_service(request: Request):
    if not hasattr(request.app.state, "location_service"):
        request.app.state.location_service = LocationService(generate_predefined_locations())
    return request.app.state.location_service

def get_location_service_test():
    return LocationService([])  # or LocationService(generate_test_locations())
