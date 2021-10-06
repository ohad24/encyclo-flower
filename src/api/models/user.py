from models.base import DBBaseModel
from pydantic import Field


class User(DBBaseModel):
    user_id: int = Field()
    username: str = Field()
    full_name: str = Field()
    email: str = Field()
    hashed_password: str = Field()
    is_active: bool
    is_superuser: bool
