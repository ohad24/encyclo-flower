from typing import Optional, Dict, Literal, List
from pydantic import BaseModel, Field, EmailStr, SecretStr
from models.helpers import user_id_generator, email_verification_token
from datetime import datetime
from time import time
from models.base import BaseUserOut
from models.user_observations import ObservationPreviewBase
from models.user_questions import QuestionPreviewBase

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


class UserPasswordIn(BaseModel):
    password: SecretStr = Field(min_length=6, max_length=50, example="123456")
    password2: SecretStr = Field(
        description="Confirm password", alias="confirm_password", example="123456"
    )


class CreateUserIn(UserBase, UserPasswordIn):
    """
    User input to create new user.
    """

    accept_terms_of_service: bool = Field(False, example=True)


class ResetPasswordIn(UserPasswordIn):
    """
    User input to reset password.
    """

    token: str


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


class FavoritePlant(BaseModel):
    plant_id: str
    heb_name: str
    science_name: str


class FavoritePlantOut(FavoritePlant):
    images: List[dict] = []  # TODO: replace dict with favorite plant image (out)


class UserInDB(UserBase):
    """
    User object in DB.

    The defaults usage is to generate new data on init,
    when the field is not set (in create new user).
    """

    user_id: str = Field(default_factory=user_id_generator)
    password: str
    password_iat: float = Field(default_factory=time)
    is_active: bool = False
    is_superuser: bool = False
    is_editor: bool = False
    email_verified: bool = False
    create_dt: datetime = Field(default_factory=datetime.utcnow)
    counters: UserCounters = UserCounters()
    favorite_plants: List[FavoritePlant] = []


class Login(BaseModel):
    """
    User input to login.
    """

    username: str
    password: str


class UserOut(BaseUserOut):
    """
    Full user attributes out.

    For user page
    """

    settlement: Optional[str]
    sex: Optional[SEX]
    create_dt: datetime
    phone: Optional[str]
    email: Optional[EmailStr]

    observations: List[ObservationPreviewBase] = []
    questions: List[QuestionPreviewBase] = []
    image_detections: List[
        dict
    ] = []  # TODO: the dict should be replace with something like(!) PlantPrediction
    favorite_plants: List[FavoritePlantOut] = []


class UserMinimalMetadataOut(BaseModel):
    user_id: Optional[str]
    username: Optional[str]
    is_superuser: Optional[bool]


class UserVerificationTokenData(BaseModel):
    user_id: str
    token: str = Field(default_factory=email_verification_token)
    create_dt: datetime = Field(default_factory=datetime.utcnow)


class UserVerificationTokenDataExt(UserVerificationTokenData):
    """
    Extended user verification token data for password reset.
    Allow only one token use. IF token is used, it will be set to True.
    """

    used: bool = False


class UserQueryParams(BaseModel):
    """
    User query - For find one user in DB.
    """

    username: str
    password_iat: dict
    email_verified: bool = True


class UserForgetPasswordRequest(BaseModel):
    """
    User input to reset password. When he forgot his password.
    """

    email: EmailStr


class CheckFavoritePlant(BaseModel):
    """
    Output for check if plant is in user's favorite plants.
    """

    is_favorite: bool
