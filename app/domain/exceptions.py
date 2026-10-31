class BookNotFoundError(Exception):
    """Raised when a book does not exist."""


class InvalidBookError(ValueError):
    """Raised when book data breaks a business rule."""