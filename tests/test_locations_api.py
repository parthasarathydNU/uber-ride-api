# tests/test_locations_api.py
import pytest
from fastapi.testclient import TestClient
from uuid import UUID, uuid4
from app.main import app
from app.services.location_service import LocationService
from app.dependencies import get_location_service_test, get_location_service
from app.models.location import Location

def override_get_location_service():
    return get_location_service_test()

app.dependency_overrides[get_location_service] = override_get_location_service

client = TestClient(app)

def test_get_locations_empty():
    response = client.get("/api/v1/locations")
    assert response.status_code == 200
    locations = response.json()
    assert len(locations) == 0

def test_get_locations_multiple():
    # Prepare test data
    test_locations = [
        Location.create(name="New York", latitude=40.7128, longitude=-74.0060),
        Location.create(name="Los Angeles", latitude=34.0522, longitude=-118.2437),
        Location.create(name="Chicago", latitude=41.8781, longitude=-87.6298)
    ]
    
    # Override the test service to return our test data
    def override_with_test_data():
        service = get_location_service_test()
        service._locations = test_locations
        return service

    app.dependency_overrides[get_location_service] = override_with_test_data

    response = client.get("/api/v1/locations")
    assert response.status_code == 200
    locations = response.json()
    assert len(locations) == 3
    assert locations[0]["name"] == "New York"
    assert locations[1]["name"] == "Los Angeles"
    assert locations[2]["name"] == "Chicago"

def test_get_locations_attributes():
    test_location = Location.create(name="Seattle", latitude=47.6062, longitude=-122.3321)
    
    def override_with_single_location():
        service = get_location_service_test()
        service._locations = [test_location]
        return service

    app.dependency_overrides[get_location_service] = override_with_single_location

    response = client.get("/api/v1/locations")
    assert response.status_code == 200
    locations = response.json()
    assert len(locations) == 1
    location = locations[0]
    assert location["name"] == "Seattle"
    assert abs(location["latitude"] - 47.6062) < 1e-4
    assert abs(location["longitude"] - (-122.3321)) < 1e-4

# def test_get_locations_error_handling():
#     def override_with_error():
#         service = get_location_service_test()
#         service.get_all_locations = lambda: [][0]  # This will raise an IndexError
#         return service

#     app.dependency_overrides[get_location_service] = override_with_error

#     response = client.get("/api/v1/locations")
#     assert response.status_code == 500
#     assert "Internal Server Error" in response.text

def test_create_location_success():
    new_location = {
        "name": "New York",
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    response = client.post("/api/v1/locations", json=new_location)
    assert response.status_code == 201
    assert isinstance(response.json(), str)  # Assuming the response is the new location ID
    

def test_create_location_invalid_data():
    invalid_location = {
        "name": "Invalid Location",
        "latitude": "not a number",  # Should be a float
        "longitude": -74.0060
    }
    response = client.post("/api/v1/locations", json=invalid_location)
    assert response.status_code == 422  # Unprocessable Entity

def test_create_location_missing_field():
    incomplete_location = {
        "name": "Incomplete Location",
        "latitude": 40.7128
        # Missing longitude
    }
    response = client.post("/api/v1/locations", json=incomplete_location)
    assert response.status_code == 422

# def test_create_location_out_of_range():
#     out_of_range_location = {
#         "name": "Out of Range",
#         "latitude": 91,  # Out of valid range (-90 to 90)
#         "longitude": -74.0060
#     }
#     response = client.post("/api/v1/locations", json=out_of_range_location)
#     assert response.status_code == 422


# def test_get_specific_location_success():
#     # Prepare a test location
#     test_id = uuid4()
#     test_location = Location(name="Test City", latitude=35.6895, longitude=139.6917)
    
#     def override_with_test_location():
#         service = get_location_service_test()
#         service._locations = [test_location]
#         return service

#     app.dependency_overrides[get_location_service] = override_with_test_location

#     response = client.get(f"/api/v1/locations/{test_id}")
#     assert response.status_code == 200
#     location_data = response.json()
#     assert location_data["id"] == str(test_id)
#     assert location_data["name"] == "Test City"
#     assert abs(location_data["latitude"] - 35.6895) < 1e-4
#     assert abs(location_data["longitude"] - 139.6917) < 1e-4



def test_get_location_not_found():
    non_existent_id = uuid4()
    response = client.get(f"/api/v1/locations/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Location not found"

def test_get_location_invalid_uuid():
    invalid_id = "not-a-uuid"
    response = client.get(f"/api/v1/locations/{invalid_id}")
    assert response.status_code == 422  # Unprocessable Entity


def test_update_location_success():
    # Prepare a test location
    test_id = uuid4()
    test_location = {
        "id": str(test_id),
        "name": "Old Name",
        "latitude": 35.6895,
        "longitude": 139.6917
    }
    def override_with_test_location():
        service = get_location_service_test()
        service._locations = [test_location]
        service.update_location = lambda id, loc: True
        return service

    app.dependency_overrides[get_location_service] = override_with_test_location

    updated_data = {"name": "New Name"}
    response = client.put(f"/api/v1/locations/{test_id}", json=updated_data)
    assert response.status_code == 201
    assert response.json() == str(test_id)

# def test_update_location_not_found():
#     non_existent_id = uuid4()
#     updated_data = {"name": "New Name"}
#     response = client.put(f"/api/v1/locations/{non_existent_id}", json=updated_data)
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Location not found"

def test_update_location_invalid_uuid():
    invalid_id = "not-a-uuid"
    updated_data = {"name": "New Name"}
    response = client.put(f"/api/v1/locations/{invalid_id}", json=updated_data)
    assert response.status_code == 422  # Unprocessable Entity

def test_update_location_empty_name():
    test_id = uuid4()
    updated_data = {"name": ""}
    response = client.put(f"/api/v1/locations/{test_id}", json=updated_data)
    assert response.status_code == 422
    assert "String should have at least 1 character" in response.text

def test_update_location_whitespace_name():
    test_id = uuid4()
    updated_data = {"name": "   "}
    response = client.put(f"/api/v1/locations/{test_id}", json=updated_data)
    assert response.status_code == 422
    assert "Name must not be empty or just whitespace" in response.text

def test_update_location_name_too_long():
    test_id = uuid4()
    updated_data = {"name": "a" * 101}  # 101 characters
    response = client.put(f"/api/v1/locations/{test_id}", json=updated_data)
    assert response.status_code == 422
    assert "String should have at most 100 characters" in response.text


# After all tests, clear the override
def teardown_module(module):
    app.dependency_overrides.clear()
