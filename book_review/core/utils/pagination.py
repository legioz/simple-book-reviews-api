from ninja.pagination import paginate, PaginationBase
from ninja import Field, Schema
from ninja.types import DictStrAny
from typing import Any
from django.db.models import QuerySet
from ninja.conf import settings


class LimitOffsetPagination(PaginationBase):
    class Input(Schema):
        limit: int = Field(settings.PAGINATION_PER_PAGE, ge=1, le=100)
        offset: int = Field(0, ge=0)

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        **params: DictStrAny,
    ) -> Any:
        offset = pagination.offset
        limit: int = pagination.limit
        return {
            "items": queryset[offset : offset + limit],
            "count": self._items_count(queryset),
        }


class PageNumberPagination(PaginationBase):
    class Input(Schema):
        page: int = Field(1, ge=1)
        page_size: int = Field(settings.PAGINATION_PER_PAGE, ge=1)

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        **params: DictStrAny,
    ) -> Any:
        offset = (pagination.page - 1) * pagination.page_size
        return {
            "items": queryset[offset : offset + pagination.page_size],
            "count": self._items_count(queryset),
        }
