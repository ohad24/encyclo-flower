from typing import Optional, Dict, Literal
from pydantic import BaseModel, Field, EmailStr, SecretStr
from models.helpers import user_id_generator
from datetime import datetime

SEX = Literal["זכר", "נקבה"]


class UserBase(BaseModel):
    """
    Basic information.
    """

    username: str = Field(min_length=5, max_length=20, example="username1")
    f_name: str = Field(min_length=2, max_length=20, example="Bob")
    l_name: str = Field(min_length=2, max_length=20, example="Salad")
    email: EmailStr
    phone: Optional[str]
    settlement: Optional[str]
    sex: Optional[SEX]


class CreateUserIn(UserBase):
    """
    User input to create new user.
    """

    password: SecretStr = Field(min_length=6, max_length=50, example="123456")
    password2: SecretStr = Field(
        description="Confirm password", alias="confirm_password", example="123456"
    )
    accept_terms_of_service: bool = Field(False, example=True)


class UpdateUserIn(BaseModel):
    """
    User input to update user.
    """

    f_name: Optional[str]
    l_name: Optional[str]
    phone: Optional[str]
    settlement: Optional[str]
    sex: Optional[SEX]


class UserCounters(BaseModel):
    image_detection: Dict[str, int] = {}
    # TODO: add login counter (per day)


class UserInDB(UserBase):
    """
    User object in DB.

    The defaults usage is to generate new data on init,
    when the field is not set (in create new user).
    """

    user_id: str = Field(default_factory=user_id_generator)
    password: str
    is_active: bool = True
    is_superuser: bool = False
    is_editor: bool = False
    create_dt: datetime = Field(default_factory=datetime.utcnow)
    counters: UserCounters = UserCounters()


class Login(BaseModel):
    """
    User input to login.
    """
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
    settlement: Optional[str]
    sex: Optional[SEX]
    create_dt: datetime

    # TODO: talk to shahar if anyone should see this information https://trello.com/c/8DqDO5Wa
    # phone: Optional[str]
    # email: EmailStr
