from fastapi import APIRouter, Depends, Response
from fastapi.responses import RedirectResponse
from typing import List, Union
from pymongo.mongo_client import MongoClient
from db import get_db
from models.user import UserOut, CreateUserIn, UserInDB, UpdateUserIn
from core.security import (
    get_password_hash,
    get_current_active_user,
    get_current_active_superuser,
)
from endpoints.helpers_tools.common_dependencies import QuerySearchPageParams
from endpoints.helpers_tools.user_dependencies import (
    validate_accept_terms_of_service,
    validate_username_and_email_not_in_db,
    validate_current_user_edit_itself,
    validate_match_password,
    get_existing_user,
)
from models.exceptions import (
    ExceptionUserNotPrivilege,
    ExceptionUserNotAuthenticated,
    ExceptionUserNotFound,
    ExceptionUserNotAllowToEditThisUser,
    ExceptionUserNotAcceptTermsOfService,
    ExceptionUserOrEmailAlreadyExists,
    ExceptionPasswordNotMatch,
    DetailUserNotFound,
)

router = APIRouter()


@router.get(
    "/",
    response_model=List[UserInDB],
    dependencies=[Depends(get_current_active_superuser)],
    summary="Get all users",
    description="Get all users. Only superusers can do this.",
    responses={
        401: {
            "description": ExceptionUserNotAuthenticated().detail,
            "model": ExceptionUserNotAuthenticated,
        },
        403: {
            "description": ExceptionUserNotPrivilege().detail,
            "model": ExceptionUserNotPrivilege,
        },
    },
)
async def read_users(
    db: MongoClient = Depends(get_db),
    search_params: QuerySearchPageParams = Depends(QuerySearchPageParams),
) -> List[UserInDB]:
    return list(db.users.find({}).skip(search_params.skip).limit(search_params.limit))


@router.get(
    "/me",
    response_class=RedirectResponse,
    summary="Get current user",
    description="Redirect to user profile",
    responses={
        401: {
            "description": ExceptionUserNotAuthenticated().detail,
            "model": ExceptionUserNotAuthenticated,
        }
    },
)
async def read_current_user(
    current_user: UserOut = Depends(get_current_active_user),
) -> RedirectResponse:
    return current_user.username


@router.get(
    "/{username}",
    response_model=UserOut,
    summary="User page",
    description="Get user basic data",
    responses={
        404: {
            "description": DetailUserNotFound().detail,
            "model": DetailUserNotFound,
        },
    },
)
async def read_user(
    user: UserOut = Depends(get_existing_user),
) -> UserOut:
    return user


@router.put(
    "/{username}",
    status_code=204,
    summary="Update current user",
    description="Update current user with shown fields",
    dependencies=[Depends(validate_current_user_edit_itself)],
    responses={
        400: {
            "description": ExceptionUserNotAllowToEditThisUser().detail,
            "model": ExceptionUserNotAllowToEditThisUser,
        },
        401: {
            "description": ExceptionUserNotAuthenticated().detail,
            "model": ExceptionUserNotAuthenticated,
        },
        404: {
            "description": ExceptionUserNotFound().detail,
            "model": ExceptionUserNotFound,
        },
    },
)
async def update_user(
    username: str,
    user_in: UpdateUserIn,
    db: MongoClient = Depends(get_db),
):
    db.users.update_one(
        {"username": username},
        {"$set": user_in.dict(exclude_none=True, exclude_unset=True)},
    )
    return Response(status_code=204)


@router.post(
    "/",
    status_code=201,
    dependencies=[
        Depends(validate_accept_terms_of_service),
        Depends(validate_username_and_email_not_in_db),
        Depends(validate_match_password),
    ],
    responses={
        400: {
            "description": "Input Validation",
            "model": Union[
                ExceptionUserNotAcceptTermsOfService,
                ExceptionUserOrEmailAlreadyExists,
                ExceptionPasswordNotMatch,
            ],
        },
    },
)
async def create_user(
    user_in: CreateUserIn,
    db: MongoClient = Depends(get_db),
):
    # TODO: add additional responses
    # TODO: add email verification

    # * hash the password
    hash_password = get_password_hash(user_in.password.get_secret_value())

    # * setup userInDB with hash password
    userInDB = UserInDB(**user_in.dict(exclude={"password"}), password=hash_password)

    # * insert user
    db.users.insert_one(userInDB.dict())

    return Response(status_code=201)
