from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Task Management API"
    }

def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Test task",
            "description": "This is a test",
            "status": "todo",
            "priority": "high"
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test task"
    assert response.json()["priority"] == "high"

def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_filter_tasks_by_status():
    response = client.get("/tasks?status=todo")

    assert response.status_code == 200

    for task in response.json():
        assert task["status"] == "todo"

def test_get_task_by_id():
    response = client.post(
        "/tasks",
        json={
            "title": "Find me",
            "description": "Test finding task",
            "status": "todo",
            "priority": "low"
        }
    )

    task_id = response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Find me"


def test_delete_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Delete me",
            "description": "Test deleting task",
            "status": "todo",
            "priority": "medium"
        }
    )

    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_update_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Old title",
            "description": "Old description",
            "status": "todo",
            "priority": "low"
        }
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "New title",
            "description": "Updated description",
            "status": "done",
            "priority": "high"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["status"] == "done"