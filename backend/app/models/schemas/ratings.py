from typing import List, Optional

from pydantic import BaseModel, Field, validator

from app.models.domain.ratings import Rating
from app.models.schemas.profiles import ProfileInResponse
from app.models.schemas.rwschema import RWSchema


class RatingForResponse(RWSchema, Rating):
    pass


class RatingInResponse(RWSchema):
    rating: RatingForResponse


class RatingInCreate(RWSchema):
    value: int
    comment: Optional[str] = None
    
    @validator('value')
    def check_rating_value(cls, v):
        if not (1 <= v <= 5):
            raise ValueError('Rating must be between 1 and 5')
        return v


class RatingInUpdate(RWSchema):
    value: Optional[int] = None
    comment: Optional[str] = None
    
    @validator('value')
    def check_rating_value(cls, v):
        if v is not None and not (1 <= v <= 5):
            raise ValueError('Rating must be between 1 and 5')
        return v


class ListOfRatingsInResponse(RWSchema):
    ratings: List[RatingForResponse]
    ratings_count: int
