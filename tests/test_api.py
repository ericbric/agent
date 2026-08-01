from fastapi.testclient import TestClient
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/")
def create_item(item: dict):
    return {"item": item}


client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "q": None}


def test_read_item_with_query():
    response = client.get("/items/1?q=test")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "q": "test"}


def test_create_item():
    response = client.post("/items/", json={"name": "test_item"})
    assert response.status_code == 200
    assert response.json() == {"item": {"name": "test_item"}}
