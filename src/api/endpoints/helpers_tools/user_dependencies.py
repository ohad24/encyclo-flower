from db import get_db
from pymongo.mongo_client import MongoClient
from models.user import CreateUserIn, UserInDB, UserBase
from fastapi import HTTPException, Depends, status
from core.security import get_current_active_user
from models.exceptions import (
    ExceptionUserNotFound,
    ExceptionUserNotAllowToEditThisUser,
    ExceptionUserNotAcceptTermsOfService,
    ExceptionUserOrEmailAlreadyExists,
    ExceptionPasswordNotMatch,
)


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


async def validate_match_password(user_in: CreateUserIn):
    if user_in.password.get_secret_value() != user_in.password2.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ExceptionPasswordNotMatch().detail,
        )


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
