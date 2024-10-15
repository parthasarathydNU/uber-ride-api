# app/api/locations.py
from random import randint

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from uuid import UUID

from pydantic.v1.utils import to_lower_camel

from app.models.Customer import Customer
from app.models.GeoUtility import GeoUtility
from app.models.RideManager import RideManager
from app.models.location import Location
from app.models.request_models.booking_request import BookingRequest
from app.services.location_service import LocationService
from app.models.request_models.update_location import UpdateLocation
from app.models.request_models.create_location import CreateLocation
from app.dependencies import get_location_service

router = APIRouter()

ride_manager = RideManager()

ride_manager.driverManager.addDriver(45, "Rohit Sharma", (42.3601, -71.0589), True)
ride_manager.driverManager.addDriver(18, "Virat Kohli", (43.1939, -71.5724), True )
ride_manager.driverManager.addDriver(10, "Sachin Tendulkar", (34.0549, -118.2426), True )

@router.post("/book-ride")
def book_ride(booking_request: BookingRequest):
    customerName = booking_request.customerName
    from_location = booking_request.from_location
    to_location = booking_request.to_location

    try:
        from_location_to_coordintes = GeoUtility.get_lat_lon(from_location)
        to_location_to_coordinates = GeoUtility.get_lat_lon(to_location)
    except ValueError as v:
        raise HTTPException(status_code=400, detail=str(v))

    customer = Customer(randint(100, 10000), customerName, from_location, to_location)

    try:
        book_ride = ride_manager.bookRide(customer, from_location_to_coordintes, to_location_to_coordinates)
    except ValueError as v:
        raise HTTPException(status_code=400, detail=str(v))


    return book_ride.getRideDetails()

@router.get("/locations", response_model=List[dict])
async def get_locations(locations_service: LocationService = Depends(get_location_service)):
    """Get all locations"""
    locations = locations_service.get_all_locations()
    return [location.to_dict() for location in locations]

@router.get("/locations/{location_id}", response_model=dict)
async def get_location(location_id: UUID, locations_service: LocationService = Depends(get_location_service)):
    """Get a specific location by ID"""
    location = locations_service.get_location_by_id(location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return location.to_dict()

@router.post("/locations", response_model=str, status_code=201)
async def create_location(location: CreateLocation, locations_service: LocationService = Depends(get_location_service)):
    """Create a new location"""
    newLocationId = locations_service.add_location(location)
    return newLocationId

@router.put("/locations/{location_id}", response_model=str, status_code=201)
async def update_location(location_id: UUID, updated_location: UpdateLocation, locations_service: LocationService = Depends(get_location_service)):
    """Update an existing location"""
    success = locations_service.update_location(location_id, updated_location)
    if not success:
        raise HTTPException(status_code=404, detail="Location not found")
    return str(location_id)

@router.delete("/locations/{location_id}", status_code=204)
async def delete_location(location_id: UUID, locations_service: LocationService = Depends(get_location_service)):
    """Delete a location"""
    success = locations_service.delete_location(location_id)
    if not success:
        raise HTTPException(status_code=404, detail="Location not found")

@router.get("/nearest-location")
async def get_nearest_location(latitude: float, longitude: float, locations_service: LocationService = Depends(get_location_service)):
    """Get the nearest location to given coordinates"""
    nearest_location = locations_service.get_nearest_location(latitude, longitude)
    if nearest_location is None:
        raise HTTPException(status_code=404, detail="No locations available")
    return nearest_location.to_dict()



