import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import book as book_model

client = TestClient(app)


def sample_book():
    return {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "publication_year": 2008,
        "price": 35.50,
        "available": True,
    }


# A fake in-memory database, so the tests never touch Neon
@pytest.fixture(autouse=True)
def fake_db(monkeypatch):
    books = {}
    counter = {"next_id": 1}

    def create_book(book):
        new = {"id": counter["next_id"], **book.model_dump()}
        books[new["id"]] = new
        counter["next_id"] += 1
        return new

    def get_all_books():
        return list(books.values())

    def get_book(book_id):
        return books.get(book_id)

    def update_book(book_id, book):
        if book_id not in books:
            return None
        books[book_id] = {"id": book_id, **book.model_dump()}
        return books[book_id]

    def delete_book(book_id):
        return books.pop(book_id, None) is not None

    monkeypatch.setattr(book_model, "create_book", create_book)
    monkeypatch.setattr(book_model, "get_all_books", get_all_books)
    monkeypatch.setattr(book_model, "get_book", get_book)
    monkeypatch.setattr(book_model, "update_book", update_book)
    monkeypatch.setattr(book_model, "delete_book", delete_book)


def test_create_book():
    response = client.post("/books", json=sample_book())
    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Clean Code"


def test_create_book_uses_defaults():
    data = {"title": "Dune", "author": "Frank Herbert", "price": 10}
    response = client.post("/books", json=data)
    assert response.status_code == 201
    assert response.json()["available"] is True
    assert response.json()["publication_year"] is None


def test_create_book_negative_price_is_rejected():
    data = sample_book()
    data["price"] = -5
    assert client.post("/books", json=data).status_code == 422


def test_create_book_missing_title_is_rejected():
    data = sample_book()
    del data["title"]
    assert client.post("/books", json=data).status_code == 422


def test_get_all_books_empty():
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_books():
    client.post("/books", json=sample_book())
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_book_by_id():
    client.post("/books", json=sample_book())
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["author"] == "Robert C. Martin"


def test_get_book_not_found():
    assert client.get("/books/999").status_code == 404


def test_invalid_book_id():
    assert client.get("/books/abc").status_code == 422


def test_update_book():
    client.post("/books", json=sample_book())
    data = sample_book()
    data["price"] = 40
    response = client.put("/books/1", json=data)
    assert response.status_code == 200
    assert response.json()["price"] == 40


def test_update_book_not_found():
    assert client.put("/books/999", json=sample_book()).status_code == 404


def test_delete_book():
    client.post("/books", json=sample_book())
    assert client.delete("/books/1").status_code == 204
    assert client.get("/books/1").status_code == 404


def test_delete_book_not_found():
    assert client.delete("/books/999").status_code == 404