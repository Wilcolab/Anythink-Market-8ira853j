from typing import List, Optional

from asyncpg import Connection, Record

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.db.repositories.profiles import ProfilesRepository
from app.models.domain.items import Item
from app.models.domain.ratings import Rating
from app.models.domain.users import User


class RatingsRepository(BaseRepository):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        self._profiles_repo = ProfilesRepository(conn)

    async def get_rating_by_id(
        self,
        *,
        rating_id: int,
        item: Item,
        user: Optional[User] = None,
    ) -> Rating:
        rating_row = await queries.get_rating_by_id_and_slug(
            self.connection,
            rating_id=rating_id,
            item_slug=item.slug,
        )
        if rating_row:
            return await self._get_rating_from_db_record(
                rating_row=rating_row,
                user_username=rating_row["user_username"],
                requested_user=user,
            )

        raise EntityDoesNotExist(
            "rating with id {0} does not exist".format(rating_id),
        )

    async def get_ratings_for_item(
        self,
        *,
        item: Item,
        user: Optional[User] = None,
    ) -> List[Rating]:
        ratings_rows = await queries.get_ratings_for_item_by_slug(
            self.connection,
            slug=item.slug,
        )
        return [
            await self._get_rating_from_db_record(
                rating_row=rating_row,
                user_username=rating_row["user_username"],
                requested_user=user,
            )
            for rating_row in ratings_rows
        ]
        
    async def get_average_rating_for_item(
        self,
        *,
        item_slug: str,
    ) -> Optional[float]:
        """Calculate the average rating for an item on the fly."""
        result = await queries.get_average_rating_for_item(
            self.connection,
            item_slug=item_slug,
        )
        # Fix the way we access the average_rating value from the database record
        if result and hasattr(result, "average_rating"):
            return result.average_rating  # Access as attribute instead of dictionary key
        return None

    async def create_rating_for_item(
        self,
        *,
        value: int,
        item: Item,
        user: User,
        comment: Optional[str] = None,
    ) -> Rating:
        # Check if the user has already rated this item
        existing_rating = await self.get_user_rating_for_item(
            item_slug=item.slug,
            user=user
        )
        
        if existing_rating:
            # Update existing rating
            return await self.update_rating(
                rating_id=existing_rating.id_,
                value=value,
                comment=comment,
                user=user
            )
        
        # Create new rating
        rating_row = await queries.create_new_rating(
            self.connection,
            value=value,
            item_slug=item.slug,
            user_username=user.username,
            comment=comment,
        )
        
        # Update ratings count (but not average)
        await queries.increment_ratings_count(
            self.connection,
            item_slug=item.slug,
        )
        
        return await self._get_rating_from_db_record(
            rating_row=rating_row,
            user_username=rating_row["user_username"],
            requested_user=user,
        )

    async def update_rating(
        self,
        *,
        rating_id: int,
        value: int,
        user: User,
        comment: Optional[str] = None,
    ) -> Rating:
        rating_row = await queries.update_rating(
            self.connection,
            rating_id=rating_id,
            value=value,
            user_username=user.username,
            comment=comment,
        )
        
        return await self._get_rating_from_db_record(
            rating_row=rating_row,
            user_username=rating_row["user_username"],
            requested_user=user,
        )

    async def delete_rating(
        self,
        *,
        rating: Rating,
    ) -> None:
        item_slug = rating.item_slug
        await queries.delete_rating_by_id(
            self.connection,
            rating_id=rating.id_,
            user_username=rating.user.username,
        )
        
        # Decrement the ratings count
        await queries.decrement_ratings_count(
            self.connection,
            item_slug=item_slug,
        )

    async def get_user_rating_for_item(
        self,
        *,
        item_slug: str,
        user: User,
    ) -> Optional[Rating]:
        rating_row = await queries.get_user_rating_for_item(
            self.connection,
            item_slug=item_slug,
            user_username=user.username,
        )
        
        if not rating_row:
            return None
            
        return await self._get_rating_from_db_record(
            rating_row=rating_row,
            user_username=rating_row["user_username"],
            requested_user=user,
        )

    async def _get_rating_from_db_record(
        self,
        *,
        rating_row: Record,
        user_username: str,
        requested_user: Optional[User],
    ) -> Rating:
        return Rating(
            id_=rating_row["id"],
            value=rating_row["value"],
            item_slug=rating_row["item_slug"],
            user=await self._profiles_repo.get_profile_by_username(
                username=user_username,
                requested_user=requested_user,
            ),
            comment=rating_row.get("comment"),
            created_at=rating_row["created_at"],
            updated_at=rating_row["updated_at"],
        )
