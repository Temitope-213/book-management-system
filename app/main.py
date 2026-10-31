import logging

import psycopg
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routes import books

logger = logging.getLogger(__name__)

app = FastAPI(title="Book Management System")
app.include_router(books.router)


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