from typing import Optional
from models.base import DBBaseModel
from pydantic import BaseModel, Field, EmailStr, SecretStr, validator
import uuid
from datetime import datetime
from enum import Enum


class Sex(str, Enum):
    male = "male"
    female = "female"


class User(DBBaseModel):
    user_id: str
    username: str
    f_name: str
    l_name: str
    email: EmailStr
    phone: Optional[str]
    settlement: Optional[str]
    sex: Optional[Sex]
    _password: SecretStr = Field(alias="password")
    is_active: bool
    is_editor: bool
    is_superuser: bool
    create_dt: datetime


class UserCreateIn(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, example="username1")
    f_name: str = Field(..., min_length=2, max_length=20, example="Bob")
    l_name: str = Field(..., min_length=2, max_length=20, example="Salad")
    phone: Optional[str] = Field(
        None, min_length=8, max_length=20, example="+123456789"
    )
    settlement: Optional[str] = Field(
        None, min_length=2, max_length=20, example="Haifa"
    )
    sex: Optional[Sex]
    email: EmailStr = Field(..., example="example@exampe.com")
    password: SecretStr = Field(..., min_length=6, max_length=50, example="123456")
    accept_terms_of_service: bool = Field(..., example=True)

    def __init__(self, **data):
        super().__init__(**data)
        object.__setattr__(self, "is_active", True)
        object.__setattr__(self, "is_superuser", False)
        object.__setattr__(self, "is_editor", False)
        object.__setattr__(self, "user_id", uuid.uuid4().hex)
        object.__setattr__(self, "create_dt", datetime.utcnow())

    @validator("accept_terms_of_service")
    def check_accept_terms_of_service(cls, v):
        if not v:
            raise ValueError("Terms of service must be accepted")


class UserCreateOut(BaseModel):
    user_id: str
    username: str
    f_name: str
    l_name: str
    phone: Optional[str]
    settlement: Optional[str]
    sex: Optional[Sex]
    email: EmailStr


class Login(BaseModel):
    username: str
    password: str


class BaseUserOut(BaseModel):
    username: str
    f_name: str
    l_name: str
    sex: Optional[Sex]
    create_dt: datetime
