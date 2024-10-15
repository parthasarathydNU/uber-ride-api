from typing import Tuple

from geopy.distance import geodesic

from app.models.DriverU import DriverU


class DriverManager:
    def __init__(self):
        self.driverMap: dict[int, DriverU] = {}

    def addDriver(self, driverId:int, driverName: str, driverLocation: Tuple[float, float], isAvailable: bool):
        self.driverMap[driverId] = DriverU(driverName, driverId, isAvailable, driverLocation )

    def getDriver(self, driverId: int) -> DriverU:
        return self.driverMap[driverId]

    def getClosestDriver(self, address: Tuple[float, float]) -> DriverU :
        available_drivers_nearby = [driver for driver in self.driverMap.values() if driver.isAvailable]
        if len(available_drivers_nearby) == 0:
            raise Exception("No drivers are nearby right now. Please try again after some time")
        driver_distance = lambda driver: geodesic(address, driver.getDriverLocation()).mi
        available_driver = min(available_drivers_nearby, key = driver_distance )
        return available_driver
