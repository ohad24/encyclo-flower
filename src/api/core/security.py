from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from core.config import get_settings
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from models.user import UserInDB, UserMinimalMetadataOut, UserQueryParams
from models.exceptions import (
    ExceptionUserNotFound,
    ExceptionLogin,
    ExceptionUserNotPrivilege,
)
from models.token import TokenData
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


def create_access_token(username: str, password_iat: float) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = TokenData(exp=expire, sub=username, iat=password_iat)
    encoded_jwt = jwt.encode(to_encode.dict(), settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def search_user_in_db_from_token(token_data: TokenData, db: MongoClient) -> dict:
    """
    Search user in db from token data
    """
    user = db.users.find_one(
        UserQueryParams(
            username=token_data.sub, password_iat={"$lte": token_data.iat}
        ).dict()
    )
    return user


def extract_data_from_token(token: str | None) -> TokenData | None:
    """
    Extract data from token.
    If not valid, return None.
    """
    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return None
        token_data = TokenData(**payload)
        return token_data
    return None


def validate_token_exists_and_not_expired(token_data: TokenData) -> bool:
    if not token_data or token_data.exp < datetime.now(token_data.exp.tzinfo):
        return True  # * something wrong with token
    return False  # * token is OK


async def get_current_user_if_exists(
    token: str | None = Depends(oauth2_scheme), db: MongoClient = Depends(get_db)
) -> UserMinimalMetadataOut:
    """
    Function to extract user from token.

    If exists, return user (username and user_id as dict).
    If not, return empty dict
    """
    token_data = extract_data_from_token(token)
    if validate_token_exists_and_not_expired(token_data):
        return UserMinimalMetadataOut()

    user = search_user_in_db_from_token(token_data, db)
    return UserMinimalMetadataOut(**user)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: MongoClient = Depends(get_db),
) -> UserInDB:
    """
    Validate the user in the token and db
    """
    token_data = extract_data_from_token(token)
    if validate_token_exists_and_not_expired(token_data):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = search_user_in_db_from_token(token_data, db)
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
    user = db.users.find_one(
        {"username": form_data.username, "is_active": True, "email_verified": True}
    )
    if not user or not verify_password(form_data.password, user.get("password")):
        raise HTTPException(
            **ExceptionLogin().dict(), status_code=status.HTTP_401_UNAUTHORIZED
        )
    return UserInDB(**user)
