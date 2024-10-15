import random
from typing import Tuple

from geopy.distance import geodesic

from app.models import Customer
from app.models.DriverManager import DriverManager
from app.models.Ride import Ride


class RideManager:
    def __init__(self):
        self.book_Details = {}
        self.driverManager = DriverManager()

    def bookRide(self, customer: Customer, source: Tuple[float, float], destination: Tuple[float, float]) -> Ride:
        available_near_driver = self.driverManager.getClosestDriver(source)
        tariff_for_the_ride = self.calculateTariff(source, destination)
        booking_id = random.randint(1, 10000)
        new_booking = Ride(booking_id,  customer, available_near_driver, tariff_for_the_ride, source, destination)
        available_near_driver.isAvailable = False
        self.book_Details[booking_id] = new_booking
        return new_booking



    def calculateTariff(self, source: Tuple[float, float], destination: Tuple[float, float]) -> float:
        return geodesic(source, destination).mi * 7


