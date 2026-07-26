from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200


def test_prediction():
    response = client.post(
        "/predict",
        json={
            "distance_km": 10,
            "traffic_level": 2
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "predicted_fare" in data