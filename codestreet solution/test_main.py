from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_disruption_detection_high_confidence():
    payload = {
        "trip_id": "TRIP-12345",
        "flight_number": "AI274",
        "disruption_type": "Cancelled",
        "reason": "Severe Weather",
        "user_automation_preference": 50 # Set low so it passes confidence check automatically
    }
    
    response = client.post("/api/v1/disruption/detect", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["trip_id"] == "TRIP-12345"
    assert data["status"] == "Recovery Plan Generated"
    assert "selected_plan" in data
    assert data["selected_plan"]["jrs_score"] > 0
    # With a threshold of 50, requires_user_approval should be false for the highest scoring mock plan
    assert data["requires_user_approval"] == False

def test_disruption_detection_low_confidence():
    payload = {
        "trip_id": "TRIP-67890",
        "flight_number": "AI274",
        "disruption_type": "Cancelled",
        "reason": "Severe Weather",
        "user_automation_preference": 100 # Set high so it requires user approval
    }
    
    response = client.post("/api/v1/disruption/detect", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    # If threshold is 100, and confidence is below 100, it asks for user approval
    assert data["requires_user_approval"] == True