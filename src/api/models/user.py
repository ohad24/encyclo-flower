from typing import Optional, Dict
from pydantic import BaseModel, Field, EmailStr, SecretStr
from models.helpers import user_id_generator
from datetime import datetime
from enum import Enum


class Sex(str, Enum):
    # TODO: change to literal
    male = "זכר"
    female = "נקבה"


class User(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, example="username1")
    f_name: str = Field(..., min_length=2, max_length=20, example="Bob")
    l_name: str = Field(..., min_length=2, max_length=20, example="Salad")
    email: EmailStr
    phone: Optional[str]
    settlement: Optional[str]
    sex: Optional[Sex]


class BaseUserIn(User):
    password: SecretStr = Field(..., min_length=6, max_length=50, example="123456")
    password2: SecretStr = Field(
        description="Confirm password", alias="confirm_password", example="123456"
    )
    accept_terms_of_service: bool = Field(False, example=True)


class UpdateUserIn(BaseModel):
    f_name: Optional[str]
    l_name: Optional[str]
    phone: Optional[str]
    settlement: Optional[str]
    sex: Optional[Sex]


class UserCounters(BaseModel):
    image_detection: Dict[str, int] = {}
    # TODO: add login counter (per day)


class UserInDB(User):
    user_id: str = Field(default_factory=user_id_generator)
    password: str
    is_active: bool = True
    is_superuser: bool = False
    is_editor: bool = False
    create_dt: datetime = Field(default_factory=datetime.utcnow)
    counters: UserCounters = UserCounters()


class Login(BaseModel):
    username: str
    password: str


class BaseUserOut(BaseModel):
    """
    For general objects. (observations, questions, comments etc.)
    """

    user_id: str
    username: str
    f_name: str
    l_name: str


class UserOut(BaseUserOut):
    """
    Full user attributes out.

    For user page
    """

    username: str
    f_name: str
    l_name: str
    phone: Optional[str]
    settlement: Optional[str]
    sex: Optional[Sex]
    create_dt: datetime
    email: EmailStr
