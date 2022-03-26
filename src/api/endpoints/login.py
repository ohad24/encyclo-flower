from time import time
from fastapi import APIRouter, Depends, Request, Response, BackgroundTasks
from core.security import create_access_token, get_user_for_login, get_password_hash
from core.config import get_settings
from models.token import Token
from models.user import UserInDB, ResetPasswordIn
from models.exceptions import (
    ExceptionLogin,
    DetailUserNotFound,
    ExceptionPasswordNotMatch,
    ExceptionUserResetPasswordTokenNotFound,
)
from db import get_db
from pymongo import MongoClient
from endpoints.helpers_tools.user_dependencies import (
    get_user_from_email,
    get_user_from_reset_password_token,
    validate_match_passwords__reset_password,
)
from endpoints.helpers_tools.email import setup_reset_password_email

settings = get_settings()

router = APIRouter()


@router.post(
    "/token",
    response_model=Token,
    summary="Login",
    description="Login using username and password",
    responses={
        401: {"description": ExceptionLogin().detail, "model": ExceptionLogin},
    },
)
def login_for_access_token(
    user: UserInDB = Depends(get_user_for_login),
) -> Token:
    access_token = create_access_token(
        user.username,
        user.password_iat,
    )
    return Token(access_token=access_token)


@router.post(
    "/reset-password-request",
    status_code=204,
    summary="Reset password request",
    description="""When the user forgot his password for login,
        he can request for reset VIA his email using this endpoint.""",
    responses={
        404: {"description": DetailUserNotFound().detail, "model": DetailUserNotFound},
    },
)
def reset_password_request(
    request: Request,
    background_tasks: BackgroundTasks,
    user: UserInDB = Depends(get_user_from_email),
):
    background_tasks.add_task(
        setup_reset_password_email,
        user.user_id,
        user.email,
        request.base_url,
    )
    return Response(status_code=204)


@router.post(
    "/reset-password",
    status_code=204,
    dependencies=[Depends(validate_match_passwords__reset_password)],
    summary="Reset password",
    description="Change user forgotten password with available reset password token.",
    responses={
        400: {
            "description": ExceptionPasswordNotMatch().detail,
            "model": ExceptionPasswordNotMatch,
        },
        404: {
            "description": ExceptionUserResetPasswordTokenNotFound().detail,
            "model": ExceptionUserResetPasswordTokenNotFound,
        },
    },
)
def reset_password(
    passwords_data: ResetPasswordIn,
    user_id: str = Depends(get_user_from_reset_password_token),
    db: MongoClient = Depends(get_db),
):
    hashed_password = get_password_hash(passwords_data.password.get_secret_value())
    db.users.update_one(
        {"user_id": user_id},
        {"$set": {"password": hashed_password, "password_iat": time()}},
    )
    db.reset_password_tokens.update_one({"user_id": user_id}, {"$set": {"used": True}})
    return Response(status_code=204)
