import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

def test_build_endpoint_invalid_url():
    response = client.post("/api/v1/build", json={"repo_url": "not-a-url"})
    assert response.status_code == 422

@patch("app.main.build_apk_task.delay")
def test_build_endpoint_success(mock_delay):
    mock_task = MagicMock()
    mock_task.id = "test-task-id"
    mock_delay.return_value = mock_task

    response = client.post("/api/v1/build", json={"repo_url": "https://github.com/user/repo.git"})
    assert response.status_code == 202
    assert response.json() == {"task_id": "test-task-id", "status": "PENDING"}

@patch("app.main.celery_app.AsyncResult")
def test_status_endpoint_pending(mock_async_result):
    mock_result = MagicMock()
    mock_result.status = "PENDING"
    mock_result.ready.return_value = False
    mock_result.info = None
    mock_async_result.return_value = mock_result

    response = client.get("/api/v1/status/test-task-id")
    assert response.status_code == 200
    assert response.json()["status"] == "PENDING"

@patch("app.main.celery_app.AsyncResult")
def test_status_endpoint_success(mock_async_result):
    mock_result = MagicMock()
    mock_result.status = "SUCCESS"
    mock_result.ready.return_value = True
    mock_result.result = {
        "status": "SUCCESS",
        "logs": "Build success logs",
        "download_url": "/api/v1/download/test-task-id"
    }
    mock_async_result.return_value = mock_result

    response = client.get("/api/v1/status/test-task-id")
    assert response.status_code == 200
    assert response.json()["status"] == "SUCCESS"
    assert response.json()["download_url"] == "/api/v1/download/test-task-id"

def test_download_endpoint_not_found():
    response = client.get("/api/v1/download/non-existent")
    assert response.status_code == 404
