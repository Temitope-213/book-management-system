from typing import List

from fastapi import APIRouter, Depends, Path, Response, status

from app.api.dependencies import (
    create_book_use_case,
    delete_book_use_case,
    get_book_use_case,
    get_books_use_case,
    update_book_use_case,
)
from app.application.use_cases.create_book import CreateBook
from app.application.use_cases.delete_book import DeleteBook
from app.application.use_cases.get_books import GetBook, GetBooks
from app.application.use_cases.update_book import UpdateBook
from app.schemas.book import BookCreate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    use_case: CreateBook = Depends(create_book_use_case),
):
    return use_case.execute(book.model_dump())


@router.get("", response_model=List[BookResponse])
def get_books(use_case: GetBooks = Depends(get_books_use_case)):
    return use_case.execute()


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int = Path(..., gt=0),
    use_case: GetBook = Depends(get_book_use_case),
):
    return use_case.execute(book_id)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book: BookCreate,
    book_id: int = Path(..., gt=0),
    use_case: UpdateBook = Depends(update_book_use_case),
):
    return use_case.execute(book_id, book.model_dump())


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int = Path(..., gt=0),
    use_case: DeleteBook = Depends(delete_book_use_case),
):
    use_case.execute(book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)