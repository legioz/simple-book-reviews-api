from core.models import User, Review
from ninja import Router
from core.API.schemas import review as schemas
from django.db.models import Avg
import logging
from core.utils.pagination import paginate, LimitOffsetPagination
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


@router.get("search", response={200: list[schemas.ReviewOut]})
@paginate(LimitOffsetPagination)
def search_for_books(request, payload: schemas.Filters):
    """
    Search for books
    """
    try:
        resp = requests.get(settings.GUTENINDEX_BOOKS_URL)
        if not resp.json():
            return 400, "Failed fetching data from API"
        # TODO filter books and build response
        filters = dict(user=request.user)
        reviews = Review.objects.filter(**filters).order_by("book_id")
        return 200, reviews
    except Exception as e:
        logger.exception(e)
        return 400, "Request failed"


@router.get("{id}", response={200: schemas.BookOut, 400: str})
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
