import db
from pymongo.mongo_client import MongoClient
from models.user import CreateUserIn, UserInDB, UserBase
from fastapi import HTTPException, Depends, status
from core.security import get_current_active_user  # TODO: move this to here ?
from fastapi.security import OAuth2PasswordRequestForm
from core.security import verify_password
from models.exceptions import ExceptionLogin


async def validate_accept_terms_of_service(user_in: CreateUserIn):
    if not user_in.accept_terms_of_service:
        raise HTTPException(status_code=400, detail="Terms of service must be accepted")


async def validate_username_and_email_not_in_db(
    user_in: CreateUserIn, db: MongoClient = Depends(db.get_db)
):
    user = db.users.find_one(
        {"$or": [{"username": user_in.username}, {"email": user_in.email}]}
    )
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username or email already exists in the system.",
        )


async def validate_current_user_edit_itself(
    username: str, current_user: UserBase = Depends(get_current_active_user)
):
    if current_user.username != username:
        raise HTTPException(
            status_code=400,
            detail="The user is not allowed to edit this user",
        )


async def validate_match_password(user_in: CreateUserIn):
    if user_in.password.get_secret_value() != user_in.password2.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )


# TODO: should move to security.py ?
async def get_user_for_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: MongoClient = Depends(db.get_db),
) -> UserInDB:
    """
    Check if the user exists and the password is correct.
    """
    user = db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user.get("password")):
        raise HTTPException(
            **ExceptionLogin().dict(), status_code=status.HTTP_401_UNAUTHORIZED
        )
    return UserInDB(**user)
