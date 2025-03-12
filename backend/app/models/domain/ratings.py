from typing import Optional

from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.rwmodel import RWModel
from app.models.domain.profiles import Profile


class Rating(IDModelMixin, DateTimeModelMixin, RWModel):
    value: int  # Rating value (e.g., 1-5)
    comment: Optional[str]  # Optional comment with the rating
    item_id: int  # The item being rated - changed to int to match DB
    user: Profile  # The user who provided the rating
