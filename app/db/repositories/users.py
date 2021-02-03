from typing import Optional

from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.users import UserInDB, User


class UsersRepository(BaseRepository):
    async def get_user_by_id(self, *, id_: int) -> UserInDB:
        user_row = await queries.get_user_by_id(self.connection, id=id_)
        if user_row:
            return UserInDB(**user_row)
        raise EntityDoesNotExist(f"User with id {id_} does not exist")

    async def get_user_by_email(self, *, email: str) -> UserInDB:
        user_row = await queries.get_user_by_email(self.connection, email=email)
        if user_row:
            return UserInDB(**user_row)
        raise EntityDoesNotExist(f"User with email {email} does not exist")

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user_row = await queries.get_user_by_username(self.connection, username=username)
        if user_row:
            return UserInDB(**user_row)
        raise EntityDoesNotExist(f"User with username {username} does not exist")

    async def create_user(self, *, username: str, email: str, password: str) -> UserInDB:
        user = UserInDB(username=username, email=email)
        user.set_password(password)
        async with self.connection.transaction():
            user_row = await queries.create_new_user(
                self.connection, username=user.username, email=user.email, salt=user.salt,
                hashed_password=user.hashed_password)
        return user.copy(update=dict(user_row))

    async def update_user(self, *, user: User, username: Optional[str] = None, email: Optional[str] = None,
                          password: Optional[str] = None, first_name: Optional[str] = None,
                          last_name: Optional[str] = None, age: Optional[int] = None,
                          bio: Optional[str] = None, image: Optional[str] = None) -> UserInDB:
        user_in_db = await self.get_user_by_username(username=user.username)
        user_in_db.username = username or user.username
        user_in_db.email = email or user.email
        user_in_db.first_name = first_name or user.first_name
        user_in_db.last_name = last_name or user.last_name
        user_in_db.age = age or user.age
        user_in_db.bio = bio or user.bio
        user_in_db.image = image or user.image
        if password:
            user_in_db.set_password(password)
        async with self.connection.transaction():
            user_in_db.updated_at = await queries.update_user_by_username(
                self.connection, username=user.username, new_username=user_in_db.username, new_email=user_in_db.email,
                new_salt=user_in_db.salt, new_password=user_in_db.hashed_password, new_first_name=user_in_db.first_name,
                new_last_name=user_in_db.last_name, new_age=user_in_db.age, new_bio=user_in_db.bio,
                new_image=user_in_db.image
            )
        return user_in_db
