from typing import List, Optional

from app.domain.entities.book import Book
from app.domain.repositories.book_repository import BookRepository
from app.infrastructure.database.connection import get_connection


def _to_book(row) -> Optional[Book]:
    # Turn a database row into a Book entity
    if row is None:
        return None
    row["price"] = float(row["price"])
    return Book(**row)


class PostgresBookRepository(BookRepository):
    def create(self, book: Book) -> Book:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO books (title, author, publication_year, price, available)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *
                    """,
                    (book.title, book.author, book.publication_year,
                     book.price, book.available),
                )
                return _to_book(cur.fetchone())

    def get_all(self) -> List[Book]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM books ORDER BY id")
                return [_to_book(row) for row in cur.fetchall()]

    def get_by_id(self, book_id: int) -> Optional[Book]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM books WHERE id = %s", (book_id,))
                return _to_book(cur.fetchone())

    def update(self, book_id: int, book: Book) -> Optional[Book]:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE books
                    SET title = %s, author = %s, publication_year = %s,
                        price = %s, available = %s
                    WHERE id = %s
                    RETURNING *
                    """,
                    (book.title, book.author, book.publication_year,
                     book.price, book.available, book_id),
                )
                return _to_book(cur.fetchone())

    def delete(self, book_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM books WHERE id = %s RETURNING id", (book_id,)
                )
                return cur.fetchone() is not None