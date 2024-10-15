from typing import Tuple
from uuid import uuid4


class Driver:
     def __init__(self, driverName: str, isAvailable: bool, driverLocation: Tuple[float, float]):
         self.driverName = driverName
         self.driverId = str(uuid4())
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