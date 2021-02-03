from typing import Optional

from app.models.domain.rwmodel import RWModel
from app.models.mixins import IDModelMixin, DateTimeModelMixin
from app.services import security


class User(RWModel):
    username: str
    email: str
    first_name: str = ""
    last_name: str = ""
    age: int = 0
    bio: str = ""
    image: Optional[str] = None


class UserInDB(IDModelMixin, DateTimeModelMixin, User):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)

    def set_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(self.salt + password)
