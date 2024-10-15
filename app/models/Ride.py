from typing import Tuple

from app.models import DriverU
from app.models.Customer import Customer


class Ride:
    def __init__(self, rideId: int, customer: Customer, driver: DriverU, price: float, source: Tuple[float, float], destination: Tuple[float, float]):
        self.rideId = rideId
        self.customer= customer
        self.driver= driver
        self.price = price
        self.source = source
        self.destination = destination

    def getRideDetails(self):
        return {
            "rideId": self.rideId,
            "customer": self.customer,
            "driver": self.driver,
            "price": self.price,
            "source": self.source,
            "destination": self.destination
        }