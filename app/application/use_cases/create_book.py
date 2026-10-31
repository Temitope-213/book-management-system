from app.domain.entities.book import Book
from app.domain.repositories.book_repository import BookRepository


class CreateBook:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def execute(self, data: dict) -> Book:
        book = Book(**data)  # the entity checks the business rules
        return self.repository.create(book)