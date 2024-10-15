from geopy import Nominatim


class GeoUtility:
    _location = None

    @staticmethod
    def get_lat_lon(address: str):

        if GeoUtility._location is None:
            GeoUtility._location = Nominatim(user_agent="Uber-API")

        latLongPoints = GeoUtility._location.geocode(address)
        if (latLongPoints):
            return (latLongPoints.latitude, latLongPoints.longitude)
        else:
            raise Exception("Coordinate Location Points not found")

