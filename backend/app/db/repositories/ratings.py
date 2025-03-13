from typing import List, Optional

from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from starlette import status
from fastapi import HTTPException

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
            # Get the username from the database using user_id
            user_row = await self.connection.fetchrow(
                "SELECT username FROM users WHERE id = $1", rating_row["user_id"]
            )
            
            return await self._get_rating_from_db_record(
                rating_row=rating_row,
                user_username=user_row["username"],
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
        
        result = []
        for rating_row in ratings_rows:
            # Get the username from the database using user_id
            user_row = await self.connection.fetchrow(
                "SELECT username FROM users WHERE id = $1", rating_row["user_id"]
            )
            
            rating = await self._get_rating_from_db_record(
                rating_row=rating_row,
                user_username=user_row["username"],
                requested_user=user,
            )
            result.append(rating)
        
        return result
        
    async def get_average_rating_for_item(
        self,
        *,
        item_slug: str,
    ) -> Optional[float]:
        """Calculate the average rating for an item on the fly."""
        results = await queries.get_average_rating_for_item(
            self.connection,
            item_slug=item_slug,
        )
        
        # Fix: results is a list, need to access the first element
        if results and len(results) > 0:
            result = results[0]
            if result["average_rating"] is not None:
                return float(result["average_rating"])
        return None

    async def create_rating_for_item(
        self, *, value: int, comment: Optional[str], item: Item, user: User
    ) -> Rating:
        # First, check if the user already rated this item
        existing_rating = await self.get_user_rating_for_item(
            item_slug=item.slug,
            user=user,
        )
        
        if existing_rating:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User has already rated this item"
            )
        
        # Get the numerical IDs from the database
        item_id = await self.connection.fetchval(
            "SELECT id FROM items WHERE slug = $1", item.slug
        )
        
        user_id = await self.connection.fetchval(
            "SELECT id FROM users WHERE username = $1", user.username
        )
        
        if not item_id or not user_id:
            raise EntityDoesNotExist("Item or user not found")

        try:
            # Use raw SQL instead of aiosql query
            rating_row = await self.connection.fetchrow(
                """
                INSERT INTO ratings (value, item_id, user_id, comment)
                VALUES ($1, $2, $3, $4)
                RETURNING id, value, item_id, user_id, comment, created_at, updated_at
                """,
                value, item_id, user_id, comment or ""
            )
            
            # Update item average rating and count using raw SQL
            await self.connection.execute(
                """
                UPDATE items i
                SET average_rating = (
                  SELECT AVG(value) FROM ratings r WHERE r.item_id = i.id
                )
                WHERE i.slug = $1
                """,
                item.slug
            )
            
            await self.connection.execute(
                """
                UPDATE items
                SET ratings_count = ratings_count + 1
                WHERE slug = $1
                """,
                item.slug
            )

            return await self._get_rating_from_db_record(
                rating_row=rating_row,
                user_username=user.username,
                requested_user=user,
            )
        except UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User has already rated this item"
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
        # Handle both item_id and item_slug formats
        item_id = None
        
        # Check if item_id is in the record
        if "item_id" in rating_row:
            item_id = rating_row["item_id"]
        # If not, get it from the database using item_slug
        elif "item_slug" in rating_row:
            item_id = await self.connection.fetchval(
                "SELECT id FROM items WHERE slug = $1", rating_row["item_slug"]
            )
            if not item_id:
                raise EntityDoesNotExist(f"Item with slug {rating_row['item_slug']} not found")
        else:
            # If neither is present, raise an error
            raise ValueError("Rating record must contain either item_id or item_slug")
        
        return Rating(
            id=rating_row["id"],
            value=rating_row["value"],
            item_id=item_id,
            user=await self._profiles_repo.get_profile_by_username(
                username=user_username,
                requested_user=requested_user,
            ),
            comment=rating_row.get("comment", ""),
            created_at=rating_row["created_at"],
            updated_at=rating_row["updated_at"],
        )
