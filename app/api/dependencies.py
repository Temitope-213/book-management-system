from fastapi import Depends

from app.application.use_cases.create_book import CreateBook
from app.application.use_cases.delete_book import DeleteBook
from app.application.use_cases.get_books import GetBook, GetBooks
from app.application.use_cases.login_user import LoginUser
from app.application.use_cases.register_user import RegisterUser
from app.application.use_cases.update_book import UpdateBook
from app.domain.repositories.book_repository import BookRepository
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.repositories.postgres_book_repository import (
    PostgresBookRepository,
)
from app.infrastructure.database.repositories.postgres_user_repository import (
    PostgresUserRepository,
)


def get_book_repository() -> BookRepository:
    return PostgresBookRepository()


def get_user_repository() -> UserRepository:
    return PostgresUserRepository()


def create_book_use_case(repo: BookRepository = Depends(get_book_repository)):
    return CreateBook(repo)


def get_books_use_case(repo: BookRepository = Depends(get_book_repository)):
    return GetBooks(repo)


def get_book_use_case(repo: BookRepository = Depends(get_book_repository)):
    return GetBook(repo)


def update_book_use_case(repo: BookRepository = Depends(get_book_repository)):
    return UpdateBook(repo)


def delete_book_use_case(repo: BookRepository = Depends(get_book_repository)):
    return DeleteBook(repo)


def register_user_use_case(repo: UserRepository = Depends(get_user_repository)):
    return RegisterUser(repo)


def login_user_use_case(repo: UserRepository = Depends(get_user_repository)):
    return LoginUser(repo)