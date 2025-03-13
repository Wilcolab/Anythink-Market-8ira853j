from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.domain.ratings import Rating
from app.models.schemas.rwschema import RWSchema


class RatingInResponse(RWSchema):
    rating: Rating


class ListOfRatingsInResponse(RWSchema):
    ratings: List[Rating]
    ratings_count: int


class RatingInCreate(RWSchema):
    value: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class RatingInUpdate(RWSchema):
    value: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
