from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from typing import List
from pymongo.mongo_client import MongoClient
import db
from models.user import User, UserOut, BaseUserIn, UserInDB, UpdateUserIn
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
)

router = APIRouter()


@router.get(
    "/",
    response_model=List[User],
    dependencies=[Depends(get_current_active_superuser)],
)
async def read_users(
    db: MongoClient = Depends(db.get_db),
    search_params: QuerySearchPageParams = Depends(QuerySearchPageParams),
):
    return list(db.users.find({}).skip(search_params.skip).limit(search_params.limit))


@router.get("/me", response_class=RedirectResponse)
async def read_current_user(
    current_user: User = Depends(get_current_active_user),
):
    return current_user.username


@router.get("/{username}", response_model=UserOut)
async def read_user(
    username: str,
    db: MongoClient = Depends(db.get_db),
):
    user = db.users.find_one({"username": username})
    return user


@router.put(
    "/{username}",
    status_code=204,
    summary="Update current user",
    description="Update current user with shown fields",
    dependencies=[Depends(validate_current_user_edit_itself)]
)
async def update_user(
    username: str,
    user_in: UpdateUserIn,
    db: MongoClient = Depends(db.get_db),
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
    ],
)
async def create_user(
    user_in: BaseUserIn,
    db: MongoClient = Depends(db.get_db),
):
    # TODO: add additional responses
    # TODO: add password checking (1 and 2 is matching)
    # TODO: add email verification

    # * hash the password
    hash_password = get_password_hash(user_in.password.get_secret_value())

    # * setup userInDB with hash password
    userInDB = UserInDB(**user_in.dict(exclude={"password"}), password=hash_password)

    # * insert user
    db.users.insert_one(userInDB.dict())

    return Response(status_code=201)
