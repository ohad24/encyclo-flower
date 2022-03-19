from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from core.config import get_settings
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from models.user import UserInDB, UserMinimalMetadataOut
from models.exceptions import (
    ExceptionUserNotFound,
    ExceptionLogin,
    ExceptionUserNotPrivilege,
)
from pymongo.mongo_client import MongoClient
from db import get_db

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_PREFIX}/token", auto_error=False
)

ALGORITHM = "HS256"


e403 = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=ExceptionUserNotPrivilege().detail,
)


def create_access_token(username: str, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "username": username}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def extract_username_from_token(token: str) -> str:
    """
    It might brake if the token is not valid.
    Run this with a try/except block.
    """
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("username")
    return username


async def get_current_user_if_exists(
    token: str = Depends(oauth2_scheme), db: MongoClient = Depends(get_db)
) -> UserMinimalMetadataOut:
    """
    Function to extract user from token.

    If exists, return user (username and user_id as dict).
    If not, return empty dict
    """
    try:
        username = extract_username_from_token(token)
    except (JWTError, AttributeError):
        return UserMinimalMetadataOut()

    user_data = db.users.find_one(
        {"username": username},
        {"_id": 0, "username": 1, "user_id": 1, "is_superuser": 1},
    )
    return UserMinimalMetadataOut(**user_data)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: MongoClient = Depends(get_db)
) -> UserInDB:
    """
    Validate the user in the token and db
    """
    try:
        username = extract_username_from_token(token)
    except (JWTError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.users.find_one({"username": username})
    if not user:
        raise HTTPException(**ExceptionUserNotFound().dict())
    return UserInDB(**user)


async def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user),
) -> UserInDB:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: UserInDB = Depends(get_current_active_user),
) -> UserInDB:
    if not current_user.is_superuser:
        raise e403
    return current_user


async def get_current_active_editor(
    current_user: UserInDB = Depends(get_current_active_user),
) -> UserInDB:
    if not current_user.is_editor:
        raise e403
    return current_user


def check_privilege_user(
    current_user: UserInDB,
) -> UserInDB:
    if not current_user.is_superuser | current_user.is_editor:
        return False
    return True


async def get_current_privilege_user(
    current_user: UserInDB = Depends(get_current_active_user),
) -> UserInDB:
    if not check_privilege_user(current_user):
        raise e403
    return current_user


async def get_user_for_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: MongoClient = Depends(get_db),
) -> UserInDB:
    """
    Login dependency.

    Check if the user exists and the password is correct.
    """
    user = db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user.get("password")):
        raise HTTPException(
            **ExceptionLogin().dict(), status_code=status.HTTP_401_UNAUTHORIZED
        )
    return UserInDB(**user)
