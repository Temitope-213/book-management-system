from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.application.use_cases.create_book import CreateBook
from app.application.use_cases.delete_book import DeleteBook
from app.application.use_cases.get_books import GetBook, GetBooks
from app.application.use_cases.login_user import LoginUser
from app.application.use_cases.register_user import RegisterUser
from app.application.use_cases.update_book import UpdateBook
from app.core.security import decode_access_token
from app.domain.entities.user import User
from app.domain.repositories.book_repository import BookRepository
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.repositories.postgres_book_repository import (
    PostgresBookRepository,
)
from app.infrastructure.database.repositories.postgres_user_repository import (
    PostgresUserRepository,
)

# Reads the "Authorization: Bearer <token>" header
bearer_scheme = HTTPBearer(auto_error=False)


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


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    repo: UserRepository = Depends(get_user_repository),
) -> User:
    # One message for every failure, so attackers learn nothing
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:  # no token was sent
        raise unauthorized
    user_id = decode_access_token(credentials.credentials)
    if user_id is None:  # fake, tampered or expired token
        raise unauthorized
    user = repo.get_by_id(user_id)
    if user is None:  # the account no longer exists
        raise unauthorized
    return user