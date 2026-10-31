from dataclasses import dataclass
from typing import Optional

from app.domain.exceptions import InvalidBookError


@dataclass
class Book:
    title: str
    author: str
    price: float
    publication_year: Optional[int] = None
    available: bool = True
    id: Optional[int] = None

    def __post_init__(self):
        # Business rules: these hold however the book is created
        if not self.title or len(self.title) > 200:
            raise InvalidBookError("Title is required (maximum 200 characters)")
        if not self.author or len(self.author) > 150:
            raise InvalidBookError("Author is required (maximum 150 characters)")
        if self.price < 0:
            raise InvalidBookError("Price cannot be negative")