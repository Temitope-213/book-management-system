import logging

import psycopg
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import auth, books, admin
from app.domain.exceptions import (
    BookNotFoundError,
    EmailAlreadyExistsError,
    InvalidBookError,
    InvalidCredentialsError,
)



logger = logging.getLogger(__name__)

app = FastAPI(title="Book Management System")
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(admin.router)


@app.exception_handler(BookNotFoundError)
async def book_not_found(request: Request, exc: BookNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "Book not found"})


@app.exception_handler(InvalidBookError)
async def invalid_book(request: Request, exc: InvalidBookError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(EmailAlreadyExistsError)
async def email_exists(request: Request, exc: EmailAlreadyExistsError):
    return JSONResponse(
        status_code=409, content={"detail": "Email is already registered"}
    )


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Incorrect email or password"},
        headers={"WWW-Authenticate": "Bearer"},
    )


# Database is unreachable: tell the client without revealing details
@app.exception_handler(psycopg.OperationalError)
async def db_connection_error(request: Request, exc: psycopg.OperationalError):
    logger.error("Database connection error")
    return JSONResponse(status_code=503, content={"detail": "Database unavailable"})


# Any other database error: generic message only
@app.exception_handler(psycopg.Error)
async def db_error(request: Request, exc: psycopg.Error):
    logger.error("Database error: %s", type(exc).__name__)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
