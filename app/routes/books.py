from typing import List

from fastapi import APIRouter, HTTPException, Path, Response, status

from app.models import book as book_model
from app.schemas.book import BookCreate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    return book_model.create_book(book)


@router.get("", response_model=List[BookResponse])
def get_books():
    return book_model.get_all_books()


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int = Path(..., gt=0)):
    book = book_model.get_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book: BookCreate, book_id: int = Path(..., gt=0)):
    updated = book_model.update_book(book_id, book)
    if updated is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int = Path(..., gt=0)):
    if not book_model.delete_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)