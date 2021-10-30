from models.base import DBBaseModel
from pydantic import BaseModel, Field, EmailStr, SecretStr
import uuid
from datetime import datetime

# from bson import ObjectId


class User(DBBaseModel):
    user_id: str
    username: str
    full_name: str
    email: str
    _password: SecretStr = Field(alias="password")
    is_active: bool
    is_superuser: bool
    create_dt: datetime


class UserCreateIn(BaseModel):
    username: str = Field(..., min_length=6, max_length=50, example="username1")
    full_name: str = Field(..., min_length=6, max_length=50, example="Bob Salad")
    email: EmailStr = Field(..., example="example@exampe.com")
    password: SecretStr = Field(..., min_length=6, max_length=50, example="123456")

    def __init__(self, **data):
        super().__init__(**data)
        object.__setattr__(self, "is_active", True)
        object.__setattr__(self, "is_superuser", False)
        object.__setattr__(self, "user_id", uuid.uuid4().hex)
        object.__setattr__(self, "create_dt", datetime.utcnow())


class UserCreateOut(BaseModel):
    user_id: str
    username: str
    full_name: str
    email: EmailStr


class Login(BaseModel):
    username: str
    password: str
