import logging

import psycopg
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import books
from app.domain.exceptions import BookNotFoundError, InvalidBookError

logger = logging.getLogger(__name__)

app = FastAPI(title="Book Management System")
app.include_router(books.router)


@app.exception_handler(BookNotFoundError)
async def book_not_found(request: Request, exc: BookNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "Book not found"})


@app.exception_handler(InvalidBookError)
async def invalid_book(request: Request, exc: InvalidBookError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})


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