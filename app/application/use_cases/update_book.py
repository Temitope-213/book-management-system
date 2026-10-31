from app.domain.entities.book import Book
from app.domain.exceptions import BookNotFoundError
from app.domain.repositories.book_repository import BookRepository


class UpdateBook:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def execute(self, book_id: int, data: dict) -> Book:
        book = Book(**data)
        updated = self.repository.update(book_id, book)
        if updated is None:
            raise BookNotFoundError()
        return updated