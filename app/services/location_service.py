# app/services/location_service.py

from typing import List, Optional
from uuid import UUID, uuid4
from app.models.location import Location
from app.models.request_models.create_location import CreateLocation

class LocationService:
    def __init__(self, initial_locations: List[Location]):
        self._locations = initial_locations

    def get_all_locations(self) -> List[Location]:
        """Return all locations."""
        return self._locations

    def get_location_by_id(self, location_id: UUID) -> Optional[Location]:
        """Return a location by its ID, or None if not found."""
        return next((loc for loc in self._locations if loc.id == location_id), None)

    def add_location(self, location: CreateLocation) -> str:
        """Add a new location to the list."""
        newLocation = Location.create(location.name, location.latitude, location.longitude)
        self._locations.append(newLocation)
        return str(newLocation.id)

    def update_location(self, location_id: UUID, updated_location: Location) -> bool:
        """
        Update an existing location.
        Returns True if the location was found and updated, False otherwise.
        """
        for i, loc in enumerate(self._locations):
            if loc.id == location_id:
                self._locations[i].name = updated_location.name
                return True
        return False

    def delete_location(self, location_id: UUID) -> bool:
        """
        Delete a location by its ID.
        Returns True if the location was found and deleted, False otherwise.
        """
        initial_length = len(self._locations)
        self._locations = [loc for loc in self._locations if loc.id != location_id]
        return len(self._locations) < initial_length

    def get_nearest_location(self, latitude: float, longitude: float) -> Optional[Location]:
        """
        Find the nearest location to the given coordinates.
        This is a simple implementation and doesn't account for Earth's curvature.
        """
        if not self._locations:
            return None
        
        def distance(loc: Location) -> float:
            return ((loc.latitude - latitude) ** 2 + (loc.longitude - longitude) ** 2) ** 0.5
        
        return min(self._locations, key=distance)
