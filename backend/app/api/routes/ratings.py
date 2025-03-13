from typing import Optional

from fastapi import APIRouter, Body, Depends, Response
from starlette import status

from app.api.dependencies.items import get_item_by_slug_from_path
from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.ratings import get_rating_by_id_from_path, check_rating_modification_permissions
from app.api.dependencies.database import get_repository
from app.db.repositories.ratings import RatingsRepository
from app.models.domain.items import Item
from app.models.domain.ratings import Rating
from app.models.domain.users import User
from app.models.schemas.ratings import (
    RatingInCreate,
    RatingInResponse,
    ListOfRatingsInResponse,
    RatingInUpdate,
)

router = APIRouter()


@router.get(
    "",
    response_model=ListOfRatingsInResponse,
    name="ratings:get-ratings-for-item",
)
async def list_ratings_for_item(
    item: Item = Depends(get_item_by_slug_from_path),
    user: Optional[User] = Depends(get_current_user_authorizer(required=False)),
    ratings_repo: RatingsRepository = Depends(get_repository(RatingsRepository)),
) -> ListOfRatingsInResponse:
    ratings = await ratings_repo.get_ratings_for_item(item=item, user=user)
    return ListOfRatingsInResponse(
        ratings=ratings,
        ratings_count=len(ratings)
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=RatingInResponse,
    name="ratings:rate-item",
)
async def rate_item(
    rating_create: RatingInCreate = Body(..., embed=True, alias="rating"),
    item: Item = Depends(get_item_by_slug_from_path),
    user: User = Depends(get_current_user_authorizer()),
    ratings_repo: RatingsRepository = Depends(get_repository(RatingsRepository)),
) -> RatingInResponse:
    rating = await ratings_repo.create_rating_for_item(
        value=rating_create.value,
        comment=rating_create.comment,
        item=item,
        user=user,
    )
    return RatingInResponse(rating=rating)


@router.put(
    "/{rating_id}",
    response_model=RatingInResponse,
    name="ratings:update-rating",
)
async def update_rating(
    rating_update: RatingInUpdate = Body(..., embed=True, alias="rating"),
    rating: Rating = Depends(check_rating_modification_permissions),
    ratings_repo: RatingsRepository = Depends(get_repository(RatingsRepository)),
    user: User = Depends(get_current_user_authorizer()),
) -> RatingInResponse:
    updated_rating = await ratings_repo.update_rating(
        rating_id=rating.id_,
        value=rating_update.value or rating.value,
        comment=rating_update.comment if rating_update.comment is not None else rating.comment,
        user=user,
    )
    return RatingInResponse(rating=updated_rating)


@router.delete(
    "/{rating_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="ratings:delete-rating",
    response_class=Response,
)
async def delete_rating(
    rating: Rating = Depends(check_rating_modification_permissions),
    ratings_repo: RatingsRepository = Depends(get_repository(RatingsRepository)),
) -> None:
    await ratings_repo.delete_rating(rating=rating)
