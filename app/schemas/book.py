from typing import Optional
from pydantic import BaseModel, Field

# What the user sendas when creating or updating a book
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1,max_length=200)
    author: str = Field(..., min_length=1,max_length=150)
    publication_year: Optional[int] = None # optional
    price: float = Field(..., ge=0) # greater than or equal to 0
    available: bool = True # default value is True

# What the API sends back (the same fields plus the generated ID)
class BookResponse(BookCreate):
    id: int