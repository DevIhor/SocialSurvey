from typing import Optional

from pydantic import EmailStr

from app.models.domain.users import User
from app.models.schemas.rwschema import RWSchema


class UserInLogin(RWSchema):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str


class UserInUpdate(UserInCreate):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None


class UserWithToken(User):
    token: str


class UserInResponse(RWSchema):
    user: UserWithToken
