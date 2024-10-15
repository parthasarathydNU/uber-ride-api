from uuid import uuid4

from rtree import index
from geopy.distance import geodesic
from typing import Tuple, Dict

from app.models.Driver import Driver


class DriverManager:
    def __init__(self):
        self.drivers: Dict[str, Driver] = {}
        self.rtree_index = index.Index()
        self.id_counter = 0

    def addDriver(self, driver: Driver):
        self.drivers[driver.driverId] = driver
        self.id_counter += 1
        self.rtree_index.insert(self.id_counter, (*driver.driverLocation, *driver.driverLocation), obj=driver.driverId)

    def updateDriverAvailability(self, driverId: str, isAvailable: bool):
        if driverId in self.drivers:
            self.drivers[driverId].isAvailable = isAvailable

    def getClosestDriver(self, address: Tuple[float, float]) -> Driver:
        nearest_ids = list(self.rtree_index.nearest((*address, *address), 2, objects="raw"))
        available_drivers = [self.drivers[driverId] for driverId in nearest_ids if
                             self.drivers[driverId].isAvailable]

        if not available_drivers:
            raise Exception("No drivers are nearby right now. Please try again after some time")

        return min(available_drivers, key=lambda d: geodesic(address, d.getDriverLocation()).miles)