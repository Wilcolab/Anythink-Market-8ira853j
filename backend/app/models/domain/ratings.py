from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.domain.profiles import Profile
from app.models.domain.rwmodel import RWModel


class Rating(IDModelMixin, DateTimeModelMixin, RWModel):
    value: int  # Rating value (e.g., 1-5)
    item_slug: str  # The item being rated
    user: Profile  # User who left the rating
    comment: str = None  # Optional comment with the rating
