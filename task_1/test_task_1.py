import pytest
import main
from fastapi.testclient import TestClient


client = TestClient(main.app)

JSON_PAYLOADS = {
    "valid_data": {
        "case1": {"task_title": "task #1", "task_description": "task #1 description"},
        "case2": {"task_title": "task #2", "task_description": "task #2 description", "status": True},
        "case3": {"task_title": "task #3", "task_description": "task #3 description", "status": True},
    },
    "invalid_data": {
        "case1": {"task_description": "task #1 description"},
        "case2": {"task_title": "task #2"},
        "case3": {"task_title": 123, "task_description": "task #1 description"},
    }
}

BASE_URL = "http://localhost:8000"


@pytest.mark.parametrize("case", JSON_PAYLOADS["valid_data"])
def test_valid_post_data(case):
    payload = JSON_PAYLOADS["valid_data"][case]
    expected_status = payload.get("status", False)
    response = client.post(f"{BASE_URL}/tasks", json=payload)
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["task"]["status"] == expected_status


@pytest.mark.parametrize("case", JSON_PAYLOADS["invalid_data"])
def test_invalid_post_data(case):
    payload = JSON_PAYLOADS["invalid_data"][case]
    response = client.post(f"{BASE_URL}/tasks", json=payload)
    assert response.status_code == 422


def test_get_data():
    response = client.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, dict)


def test_update_full_data():
    response = client.put(f"{BASE_URL}/tasks/2", json={"task_title": "task #20", "task_description": "task #20 description"})
    assert response.status_code == 200
    response_data = response.json()
    expected_status = False
    assert response_data["task"]["status"] == expected_status


def test_update_partial_data():
    response = client.patch(f"{BASE_URL}/tasks/3", json={"task_description": "test patch method"})
    assert response.status_code == 200
    response_data = response.json()
    expected_status = True
    assert response_data["task"]["status"] == expected_status
    assert response_data["task"]["task_description"] == "test patch method"


def test_delete_data():
    response = client.delete(f"{BASE_URL}/tasks/2")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == 2
