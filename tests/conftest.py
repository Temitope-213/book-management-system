import os

# Safe dummy values so the app can import without your real .env
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-not-for-production-0123456789abcdef")
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test")

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_book_repository, get_user_repository
from app.domain.entities.book import Book
from app.domain.entities.user import User
from app.domain.repositories.book_repository import BookRepository
from app.domain.repositories.user_repository import UserRepository
from app.main import app


class FakeUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
        self.next_id = 1

    def create(self, user: User) -> User:
        user.id = self.next_id
        user.created_at = datetime.now(timezone.utc)
        self.users[user.id] = user
        self.next_id += 1
        return user

    def get_by_email(self, email: str):
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def get_by_id(self, user_id: int):
        return self.users.get(user_id)


class FakeBookRepository(BookRepository):
    def __init__(self):
        self.books = {}
        self.next_id = 1

    def create(self, book: Book) -> Book:
        book.id = self.next_id
        self.books[book.id] = book
        self.next_id += 1
        return book

    def get_all(self):
        return list(self.books.values())

    def get_by_id(self, book_id: int):
        return self.books.get(book_id)

    def update(self, book_id: int, book: Book):
        if book_id not in self.books:
            return None
        book.id = book_id
        self.books[book_id] = book
        return book

    def delete(self, book_id: int) -> bool:
        return self.books.pop(book_id, None) is not None


@pytest.fixture
def user_repo():
    return FakeUserRepository()


@pytest.fixture
def book_repo():
    return FakeBookRepository()


@pytest.fixture
def client(user_repo, book_repo):
    app.dependency_overrides[get_user_repository] = lambda: user_repo
    app.dependency_overrides[get_book_repository] = lambda: book_repo
    yield TestClient(app)
    app.dependency_overrides.clear()


PASSWORD = "StrongPass123!"


def register_and_login(client, email, username="tester"):
    client.post(
        "/auth/register",
        json={"username": username, "email": email, "password": PASSWORD},
    )
    response = client.post(
        "/auth/login", json={"email": email, "password": PASSWORD}
    )
    return response.json()["access_token"]


@pytest.fixture
def user_headers(client):
    token = register_and_login(client, "user@example.com", "regular")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, user_repo):
    client.post(
        "/auth/register",
        json={"username": "boss", "email": "admin@example.com", "password": PASSWORD},
    )
    # Promote directly in the fake repo (same idea as the SQL UPDATE in Neon)
    user_repo.get_by_email("admin@example.com").role = "admin"
    response = client.post(
        "/auth/login", json={"email": "admin@example.com", "password": PASSWORD}
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def sample_book():
    return {"title": "Clean Code", "author": "Robert C. Martin", "price": 25.5}