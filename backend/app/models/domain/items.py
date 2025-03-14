from typing import List, Optional

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.profiles import Profile
from app.models.domain.rwmodel import RWModel


class Item(IDModelMixin, DateTimeModelMixin, RWModel):
    slug: str
    title: str
    description: str
    tags: List[str]
    seller: Profile
    favorited: bool
    favorites_count: int
    image: Optional[str]
    body: Optional[str]
    # Rating fields - average_rating is calculated on the fly
    average_rating: Optional[float] = None
    ratings_count: int = 0
