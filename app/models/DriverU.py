from typing import Tuple


class DriverU:
     def __init__(self, driverName: str, driverId: int, isAvailable: bool, driverLocation: Tuple[float, float]):
         self.driverName = driverName
         self.driverId = driverId
         self.isAvailable = isAvailable
         self.driverLocation = driverLocation

     def getDriverId(self) -> int :
         return self.driverId

     def getDriverName(self) -> str:
         return self.driverName

     def getIsAvailable(self)-> bool :
         return self.isAvailable

     def getDriverLocation(self) -> Tuple[float, float]:
         return self.driverLocation