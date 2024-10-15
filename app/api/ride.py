# app/ride.py

from fastapi import APIRouter, HTTPException

from app.models.Customer import Customer
from app.models.Driver import Driver
from app.models.GeoUtility import GeoUtility
from app.models.RideManager import RideManager
from app.models.request_models.booking_request import BookingRequest


router = APIRouter()

ride_manager = RideManager()
driver1= Driver("Rohit Sharma", True, (42.3601, -71.0589))
driver2= Driver("Virat Kohli", True, (43.1939, -71.5724) )

driver3= Driver("Sachin Tendulkar",  True, (34.0549, -118.2426))

ride_manager.driverManager.addDriver(driver1)
ride_manager.driverManager.addDriver(driver2)
ride_manager.driverManager.addDriver(driver3)

@router.get("/ride")
async def initializeRide():
    """Get all locations"""
    return {"message": "Welcome to Uber"}

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

    customer = Customer(customerName, from_location, to_location)

    try:
        book_ride = ride_manager.bookRide(customer, from_location_to_coordintes, to_location_to_coordinates)
    except ValueError as v:
        raise HTTPException(status_code=400, detail=str(v))


    return book_ride.getRideDetails()
