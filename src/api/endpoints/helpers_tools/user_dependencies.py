from db import get_db
from pymongo.mongo_client import MongoClient
from models.user import (
    CreateUserIn,
    UserInDB,
    UserBase,
    UserPasswordIn,
    ResetPasswordIn,
    UserForgetPasswordRequest,
)
from fastapi import HTTPException, Depends, status
from core.security import get_current_active_user
from models.exceptions import (
    ExceptionUserNotFound,
    ExceptionUserNotAllowToEditThisUser,
    ExceptionUserNotAcceptTermsOfService,
    ExceptionUserOrEmailAlreadyExists,
    ExceptionPasswordNotMatch,
    ExceptionUserResetPasswordTokenNotFound,
    ExceptionEmailVerificationTokenNotFound,
)
from datetime import timedelta, datetime
from core.config import get_settings
from pydantic import SecretStr

settings = get_settings()


async def validate_accept_terms_of_service(user_in: CreateUserIn):
    if not user_in.accept_terms_of_service:
        raise HTTPException(
            status_code=400, detail=ExceptionUserNotAcceptTermsOfService().detail
        )


async def validate_username_and_email_not_in_db(
    user_in: CreateUserIn, db: MongoClient = Depends(get_db)
):
    user = db.users.find_one(
        {"$or": [{"username": user_in.username}, {"email": user_in.email}]}
    )
    if user:
        raise HTTPException(
            status_code=400,
            detail=ExceptionUserOrEmailAlreadyExists().detail,
        )


async def validate_current_user_edit_itself(
    username: str, current_user: UserBase = Depends(get_current_active_user)
):
    if current_user.username != username:
        raise HTTPException(
            status_code=400,
            detail=ExceptionUserNotAllowToEditThisUser().detail,
        )


def check_matching_passwords(password: SecretStr, confirm_password: SecretStr):
    """
    Check if password and confirm password match.
    """
    if password.get_secret_value() != confirm_password.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ExceptionPasswordNotMatch().detail,
        )


async def validate_match_passwords__new_user(user_in: CreateUserIn):
    check_matching_passwords(user_in.password, user_in.password2)


async def validate_match_passwords__reset_password(passwords_data: UserPasswordIn):
    check_matching_passwords(passwords_data.password, passwords_data.password2)


async def get_existing_user(
    username: str, db: MongoClient = Depends(get_db)
) -> UserInDB:
    """
    Check if given user is exists in DB.
    """
    user = db.users.find_one({"username": username})
    if not user:
        raise HTTPException(**ExceptionUserNotFound().dict())
    return UserInDB(**user)


async def get_user_from_email_registration_token(
    token: str, db: MongoClient = Depends(get_db)
) -> str:
    """
    Validate email registration token and return username.
    """

    verification_data = db.email_verification_tokens.find_one({"token": token})
    expiration_minutes = timedelta(minutes=settings.EMAIL_VERIFICATION_EXPIRES_MINUTES)
    if (
        not verification_data
        or verification_data["create_dt"] + expiration_minutes < datetime.utcnow()
    ):
        raise HTTPException(
            status_code=404, detail=ExceptionEmailVerificationTokenNotFound().detail
        )
    return verification_data["user_id"]


async def get_user_from_email(
    email: UserForgetPasswordRequest, db: MongoClient = Depends(get_db)
) -> UserInDB:
    """
    Validate email and return user.
    """
    user = db.users.find_one({"email": email.email})
    if not user:
        raise HTTPException(**ExceptionUserNotFound().dict())
    return UserInDB(**user)


async def get_user_from_reset_password_token(
    passwords_data: ResetPasswordIn, db: MongoClient = Depends(get_db)
) -> str:
    """
    Validate reset password token and return username.
    """

    verification_data = db.reset_password_tokens.find_one(
        {"token": passwords_data.token, "used": False}
    )
    expiration_minutes = timedelta(
        minutes=settings.EMAIL_PASSWORD_RESET_EXPIRES_MINUTES
    )
    if (
        not verification_data
        or verification_data["create_dt"] + expiration_minutes < datetime.utcnow()
    ):
        raise HTTPException(
            status_code=404, detail=ExceptionUserResetPasswordTokenNotFound().detail
        )
    return verification_data["user_id"]
