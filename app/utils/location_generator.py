from dataclasses import dataclass
from typing import List
from app.models.location import Location

def generate_predefined_locations() -> List[Location]:
    predefined_locations = [
        ("Downtown", 40.7128, -74.0060),
        ("Central Park", 40.7829, -73.9654),
        ("Times Square", 40.7580, -73.9855),
        ("Brooklyn Bridge", 40.7061, -73.9969),
        ("Empire State Building", 40.7484, -73.9857),
        ("Statue of Liberty", 40.6892, -74.0445),
        ("High Line", 40.7480, -74.0048),
        ("Wall Street", 40.7068, -74.0090),
        ("Greenwich Village", 40.7335, -74.0027),
        ("Chinatown", 40.7159, -73.9977),
        ("SoHo", 40.7233, -74.0030),
        ("Little Italy", 40.7191, -73.9973),
        ("Rockefeller Center", 40.7587, -73.9787),
        ("Metropolitan Museum of Art", 40.7794, -73.9632),
        ("Broadway Theater District", 40.7590, -73.9845),
        ("Madison Square Garden", 40.7505, -73.9934),
        ("One World Trade Center", 40.7127, -74.0134),
        ("Columbia University", 40.8075, -73.9626),
        ("Yankees Stadium", 40.8296, -73.9262),
        ("Coney Island", 40.5755, -73.9707),
    ]
    
    return [Location.create(name, lat, lon) for name, lat, lon in predefined_locations]
