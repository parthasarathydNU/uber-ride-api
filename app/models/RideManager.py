import random
from functools import lru_cache
from typing import Tuple

from geopy.distance import geodesic

from app.models import Customer
from app.models.DriverManager import DriverManager
from app.models.Ride import Ride


class RideManager:
    def __init__(self):
        self.book_Details = {}
        self.driverManager = DriverManager()

        self.basic_fare = 8.0
        self.basic_distance = 10.0
        self.per_mile_rate = 2.5
        self.min_fare = 13.0
        self.long_trip_baseline = 50
        self.long_trip_adder = 2.0

    def bookRide(self, customer: Customer, source: Tuple[float, float], destination: Tuple[float, float]) -> Ride:
        available_near_driver = self.driverManager.getClosestDriver(source)
        tariff_for_the_ride = self.calculateTariff(source, destination)
        new_booking = Ride(customer, available_near_driver, tariff_for_the_ride, source, destination)
        self.driverManager.updateDriverAvailability(available_near_driver.driverId,False )
        new_booking.price = tariff_for_the_ride
        new_booking.distance = self.getDistance(source, destination)
        self.book_Details[new_booking.rideId] = new_booking
        return new_booking

    def getDistance(self, source, destination) -> float:
        return geodesic(source, destination).mi

    def calculateTariff(self, source: Tuple[float, float], destination: Tuple[float, float] ) -> float:
        distance_mile = self.getDistance(source, destination)


        if distance_mile <= self.basic_distance:
            return self.basic_fare

        tariff = self.basic_fare + (distance_mile  * self.per_mile_rate)

        if distance_mile > self.long_trip_baseline:
            tariff *= self.long_trip_adder

        return max(tariff, self.min_fare)

