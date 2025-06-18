from typing import TypeVar, Generic, Optional, List

from ninja import FilterSchema, Schema
from pydantic import Field


F = TypeVar("F", bound=FilterSchema)

class PaginationQueryParams(Schema, Generic[F]):
    page: int = Field(0, ge=0)
    page_size: int = Field(10, ge=1, le=1000)
    filters: Optional[F] = None
    order_by: Optional[List[str]] = None
