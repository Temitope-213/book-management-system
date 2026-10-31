from app.database.connection import get_connection

def create_book(book):
    # Save a new book; the database generates the ID
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO books (title, author, publication_year, price, available)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (book.title, book.author, book.publication_year, book.price, book.available),
            )
            return cur.fetchone()

def get_all_books():
    # Return every book (an empty list if there are none)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM books ORDER BY id")
            return cur.fetchall() 

def get_book(book_id):
    # Return a single book by ID (or None if not found)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM books WHERE id = %s", (book_id,))
            return cur.fetchone()

def update_book(book_id, book):
    # Update an existing book by ID; return the updated book (or None if not found)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE books
                SET title = %s, author = %s, publication_year = %s, price = %s, available = %s
                WHERE id = %s
                RETURNING *
                """,
                (book.title, book.author, book.publication_year, book.price, book.available, book_id),
            )
            return cur.fetchone()

def delete_book(book_id):
    # Delete a book by ID; returns book if it existed, False if not
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM books WHERE id = %s RETURNING id", (book_id,))
            return cur.fetchone() is not None