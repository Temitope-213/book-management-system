from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.book import Book


# Describes WHAT the app needs from storage, not HOW it is done
class BookRepository(ABC):
    @abstractmethod
    def create(self, book: Book) -> Book: ...

    @abstractmethod
    def get_all(self) -> List[Book]: ...

    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]: ...

    @abstractmethod
    def update(self, book_id: int, book: Book) -> Optional[Book]: ...

    @abstractmethod
    def delete(self, book_id: int) -> bool: ...