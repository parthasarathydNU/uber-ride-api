import uuid
from typing import Tuple

from app.models import Driver
from app.models.Customer import Customer


class Ride:
    def __init__(self, customer: Customer, driver: Driver, price: float, source: Tuple[float, float], destination: Tuple[float, float], distance: int = 1):
        self.rideId = str(uuid.uuid4())
        self.customer= customer
        self.driver= driver
        self.price = price
        self.source = source
        self.destination = destination
        self.distance = distance

    def getRideDetails(self):
        return {
            "rideId": self.rideId,
            "customer": self.customer,
            "driver": self.driver,
            "price": self.price,
            "source": self.source,
            "destination": self.destination,
            "distance": self.distance
        }