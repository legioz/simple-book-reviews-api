from ninja import Schema
import uuid
from pydantic import conint
from datetime import datetime, date

    
class ReviewIn(Schema):
    book_id: int
    rating: conint(gt=0, le=5)
    message: str
    

class ReviewOut(ReviewIn):
    id: uuid.UUID | None
    user_id: uuid.UUID | None
    created_at: datetime | None
    updated_at: datetime | None


class Filters(Schema):
    title: str | None = None
    book_id: int | None = None


class AuthorOut(Schema):
    name: str | None
    birth_year: date | None
    death_year: date | None


class BookReviewMessageOut(Schema):
    user_id: uuid.UUID | None
    rating: conint(gt=0, le=5) | None
    message: str | None

class BookOut(Schema):
    id: int | None
    title: str | None
    authors: list[AuthorOut] | None
    languages: list[str] | None
    download_count: int | None
    rating: float | None
    reviews: list[BookReviewMessageOut] | None
 