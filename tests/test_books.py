import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_book_repository
from app.domain.entities.book import Book
from app.domain.exceptions import InvalidBookError
from app.domain.repositories.book_repository import BookRepository
from app.main import app

client = TestClient(app)


def sample_book():
    return {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "publication_year": 2008,
        "price": 35.50,
        "available": True,
    }


# A fake in-memory repository, so the tests never touch Neon
class FakeBookRepository(BookRepository):
    def __init__(self):
        self.books = {}
        self.next_id = 1

    def create(self, book):
        book.id = self.next_id
        self.books[book.id] = book
        self.next_id += 1
        return book

    def get_all(self):
        return list(self.books.values())

    def get_by_id(self, book_id):
        return self.books.get(book_id)

    def update(self, book_id, book):
        if book_id not in self.books:
            return None
        book.id = book_id
        self.books[book_id] = book
        return book

    def delete(self, book_id):
        return self.books.pop(book_id, None) is not None


@pytest.fixture(autouse=True)
def fake_db():
    repo = FakeBookRepository()
    app.dependency_overrides[get_book_repository] = lambda: repo
    yield
    app.dependency_overrides.clear()


def test_book_entity_rejects_negative_price():
    with pytest.raises(InvalidBookError):
        Book(title="X", author="Y", price=-1)


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