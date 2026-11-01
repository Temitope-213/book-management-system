class BookNotFoundError(Exception):
    """Raised when a book does not exist."""


class InvalidBookError(ValueError):
    """Raised when book data breaks a business rule."""

class EmailAlreadyExistsError(Exception):
    """Raised when an email is already registered."""


class InvalidCredentialsError(Exception):
    """Raised when the email or password is wrong."""