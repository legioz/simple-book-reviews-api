from core.models import Review
from ninja import Router
from core.API.schemas import review as schemas
from django.db.models import Avg
import logging
from core.utils.pagination import paginate, PageNumberPagination
import requests
from django.conf import settings

logger = logging.getLogger("db")
router = Router()


@router.post("review", response={200: schemas.ReviewOut | None, 400: str})
def create_new_review(request, payload: schemas.ReviewIn):
    """
    Create a book review for the current logged user
    """
    try:
        data = payload.dict()
        data["user"] = request.user
        review = Review.objects.create(**data)
        review.save()
        return 200, review
    except Exception as e:
        logger.exception(e)
        return 400, "Could not create a new review"


@router.get("search", response={200: list[schemas.BookOutMin]}, auth=None)
@paginate(PageNumberPagination)
def search_for_books(request, title_or_author: str = None):
    """
    Search for books
    """
    try:
        filters = {}
        filters["page"] = request.GET.get("page")
        if title_or_author is not None:
            filters["search"] = title_or_author
        resp = requests.get(settings.GUTENINDEX_BOOKS_URL, params=filters)
        if resp.status_code != 200:
            return 400, "Failed fetching data from API"
        data = resp.json()
        books = []
        for book in data["results"]:
            books.append(schemas.BookOutMin.parse_obj(book))
        return books
    except Exception as e:
        logger.exception(e)
        return 400


@router.get("{id}", response={200: schemas.BookOut, 400: str}, auth=None)
def get_book_details(request, id: int):
    """
    Get book details by id
    """
    try:
        resp = requests.get(settings.GUTENINDEX_BOOKS_URL + f"{id}")
        if resp.status_code != 200:
            return 400, "Failed fetching data from API"
        details = schemas.BookOut.parse_obj(resp.json())
        reviews = Review.objects.filter(book_id=id)
        details.rating = reviews.aggregate(Avg("rating"))["rating__avg"]
        logger.info(list(reviews.values("message")))
        details.reviews = list(reviews.values("message", "rating", "user_id"))
        return 200, details
    except Exception as e:
        logger.exception(e)
        return 400, "Could get book details"
