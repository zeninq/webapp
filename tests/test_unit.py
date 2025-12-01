import json
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_add_task(client):
    r = client.post("/api/todo", json={"task": "Test Task"})
    assert r.status_code == 201


def test_get_tasks(client):
    r = client.get("/api/todo")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)
