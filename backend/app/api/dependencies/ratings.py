from typing import Optional

from fastapi import Depends, HTTPException, Path
from starlette import status

from app.api.dependencies import items, authentication, database
from app.db.errors import EntityDoesNotExist
from app.db.repositories.ratings import RatingsRepository
from app.models.domain.items import Item
from app.models.domain.ratings import Rating
from app.models.domain.users import User
from app.resources import strings


async def get_rating_by_id_from_path(
    rating_id: int = Path(..., ge=1),
    item: Item = Depends(items.get_item_by_slug_from_path),
    user: Optional[User] = Depends(
        authentication.get_current_user_authorizer(required=False),
    ),
    ratings_repo: RatingsRepository = Depends(
        database.get_repository(RatingsRepository),
    ),
) -> Rating:
    try:
        return await ratings_repo.get_rating_by_id(
            rating_id=rating_id,
            item=item,
            user=user,
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.RATING_DOES_NOT_EXIST,
        )


async def check_rating_modification_permissions(
    rating: Rating = Depends(get_rating_by_id_from_path),
    user: User = Depends(authentication.get_current_user_authorizer()),
) -> Rating:
    if rating.user.username != user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.USER_IS_NOT_AUTHOR_OF_RATING,
        )
    
    return rating
