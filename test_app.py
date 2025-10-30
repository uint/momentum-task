from fastapi.testclient import TestClient
import pytest

from app import create_app
from core.store.in_mem import InMemoryStore

@pytest.fixture()
def client():
    app = create_app(InMemoryStore())
    client = TestClient(app)
    yield client

def test_list_initially_empty(client):
    response = client.get("/book")
    assert response.status_code == 200
    assert response.json() == []

def test_add_books(client):
    book1 = {"ident": 0, "title": "foo", "author": "bar"}
    book2 = {"ident": 2, "title": "baz", "author": "bax"}

    response = client.post("/book", json=book1)
    assert response.status_code == 200
    response = client.post("/book", json=book2)
    assert response.status_code == 200

    response = client.get("/book")
    assert response.status_code == 200
    assert response.json() == [{**book1, "borrowed": None}, {**book2, "borrowed": None}]

def test_add_delete_book(client):
    book = {"ident": 0, "title": "foo", "author": "bar"}

    response = client.post("/book", json=book)

    response = client.get("/book")
    assert response.status_code == 200
    assert response.json() == [{**book, "borrowed": None}]

    response = client.delete("/book/0")
    assert response.status_code == 200

    response = client.get("/book")
    assert response.status_code == 200
    assert response.json() == []

def test_update_book(client):
    book = {"ident": 0, "title": "foo", "author": "bar"}
    borrowed = {"who": 8, "when": "2025-10-29T20:05:52.661000+00:00"}

    response = client.post("/book", json=book)

    response = client.get("/book")
    assert response.status_code == 200
    assert response.json() == [{**book, "borrowed": None}]

    response = client.put("/book/0", json={"borrowed": borrowed})
    assert response.status_code == 200

    response = client.get("/book")
    assert response.status_code == 200
    assert response.json() == [{**book, "borrowed": borrowed}]
