# tests/test_locations_api.py

import pytest
from fastapi.testclient import TestClient
from uuid import UUID
from app.main import app
from app.models.location import Location
from app.models.request_models.create_location import CreateLocation
from app.services.location_service import LocationService

client = TestClient(app)

@pytest.fixture
def location_service():
    return LocationService(initial_locations=[])

@pytest.fixture
def mock_locations(location_service):
    locations = [
        Location.create(id=UUID("a7e5c6f1-ad1d-4a8a-928f-b5b4cdd6a0a6"), name="Test Location 1", latitude=40.7128, longitude=-74.0060),
        Location.create(id=UUID("b8d6e7f2-be2e-5b9b-a39f-c6c5dee7b1b7"), name="Test Location 2", latitude=34.0522, longitude=-118.2437)
    ]
    for loc in locations:
        location_service._locations.append(loc)
    return locations

def test_create_location(location_service):
    new_location = CreateLocation(name="New Location", latitude=51.5074, longitude=-0.1278)
    response = client.post("/api/v1/locations", json=new_location.dict())
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "New Location"
    assert data["latitude"] == 51.5074
    assert data["longitude"] == -0.1278

def test_create_location_invalid_data():
    invalid_location = {"name": "", "latitude": 100, "longitude": 200}
    response = client.post("/api/v1/locations", json=invalid_location)
    assert response.status_code == 422

def test_get_all_locations(mock_locations):
    response = client.get("/api/v1/locations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Test Location 1"
    assert data[1]["name"] == "Test Location 2"

def test_get_location_by_id(mock_locations):
    location_id = str(mock_locations[0].id)
    response = client.get(f"/api/v1/locations/{location_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Location 1"

def test_get_location_by_id_not_found():
    non_existent_id = "c9f7d8e3-cf3f-6c0c-b40f-d7d6e8f9g0h1"
    response = client.get(f"/api/v1/locations/{non_existent_id}")
    assert response.status_code == 404

def test_update_location(mock_locations):
    location_id = str(mock_locations[0].id)
    updated_data = {"name": "Updated Location", "latitude": 55.7558, "longitude": 37.6173}
    response = client.put(f"/api/v1/locations/{location_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Location"
    assert data["latitude"] == 55.7558
    assert data["longitude"] == 37.6173

def test_update_location_not_found():
    non_existent_id = "c9f7d8e3-cf3f-6c0c-b40f-d7d6e8f9g0h1"
    updated_data = {"name": "Updated Location", "latitude": 55.7558, "longitude": 37.6173}
    response = client.put(f"/api/v1/locations/{non_existent_id}", json=updated_data)
    assert response.status_code == 404

def test_delete_location(mock_locations):
    location_id = str(mock_locations[0].id)
    response = client.delete(f"/api/v1/locations/{location_id}")
    assert response.status_code == 204
    
    # Verify the location has been deleted
    get_response = client.get(f"/api/v1/locations/{location_id}")
    assert get_response.status_code == 404

def test_delete_location_not_found():
    non_existent_id = "c9f7d8e3-cf3f-6c0c-b40f-d7d6e8f9g0h1"
    response = client.delete(f"/api/v1/locations/{non_existent_id}")
    assert response.status_code == 404

def test_get_nearest_location(mock_locations):
    response = client.get("/api/v1/locations/nearest?latitude=40.7&longitude=-74.0")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Location 1"

def test_get_nearest_location_empty_service(location_service):
    response = client.get("/api/v1/locations/nearest?latitude=40.7&longitude=-74.0")
    assert response.status_code == 404
    assert response.json()["detail"] == "No locations available"
