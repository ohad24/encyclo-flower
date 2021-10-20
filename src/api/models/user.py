from models.base import DBBaseModel
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import uuid

# from bson import ObjectId


class User(DBBaseModel):
    user_id: str = Field(default=None)
    username: str = Field()
    full_name: str = Field(default=None)
    email: str = Field()
    _password: str = Field(alias="password")
    is_active: bool
    is_superuser: bool


class UserCreateIn(BaseModel):
    username: str
    full_name: str
    email: Optional[EmailStr] = None
    password: str

    def __init__(self, **data):
        super().__init__(**data)
        object.__setattr__(self, "is_active", True)
        object.__setattr__(self, "is_superuser", False)
        object.__setattr__(self, "user_id", uuid.uuid4().hex)


class UserCreateOut(BaseModel):
    user_id: str
    username: str
    full_name: str
    email: EmailStr


class Login(BaseModel):
    username: str
    password: str
