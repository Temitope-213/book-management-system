from app.domain.exceptions import BookNotFoundError
from app.domain.repositories.book_repository import BookRepository


class DeleteBook:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def execute(self, book_id: int) -> None:
        if not self.repository.delete(book_id):
            raise BookNotFoundError()