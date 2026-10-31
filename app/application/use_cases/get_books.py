from typing import List

from app.domain.entities.book import Book
from app.domain.exceptions import BookNotFoundError
from app.domain.repositories.book_repository import BookRepository


class GetBooks:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def execute(self) -> List[Book]:
        return self.repository.get_all()


class GetBook:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def execute(self, book_id: int) -> Book:
        book = self.repository.get_by_id(book_id)
        if book is None:
            raise BookNotFoundError()
        return book