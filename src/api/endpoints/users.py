from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import RedirectResponse
from typing import Any, List
from pymongo.mongo_client import MongoClient
import db
import models.user as user_model
from core.security import (
    get_password_hash,
    get_current_active_user,
    get_current_active_superuser,
)

router = APIRouter()


@router.get("/", response_model=List[user_model.User])
async def read_users(
    db: MongoClient = Depends(db.get_db),
    current_user: user_model.User = Depends(get_current_active_superuser),
):
    return list(db.users.find({}))


@router.get("/me", response_class=RedirectResponse)
async def read_current_user(
    current_user: user_model.User = Depends(get_current_active_user),
):
    return current_user.username


@router.get("/{username}", response_model=user_model.BaseUserOut)
async def read_user(
    username: str,
    db: MongoClient = Depends(db.get_db),
):
    user = db.users.find_one({"username": username})
    return user


@router.put(
    "/{username}",
    response_model=user_model.BaseUserOut,
    summary="Update current user",
    description="Update current user with shown fields",
)
async def update_user(
    username: str,
    user_in: user_model.BaseUserIn,
    db: MongoClient = Depends(db.get_db),
    current_user: user_model.User = Depends(get_current_active_user),
):
    # * check if user is the same
    if current_user.username != username:
        raise HTTPException(
            status_code=400,
            detail="The user is not allowed to edit this user",
        )

    # * remove None values from user input
    user_dict = {k: v for k, v in user_in.dict().items() if v is not None}
    db.users.update_one({"username": username}, {"$set": user_dict})

    # * retrive updated user
    user_out = db.users.find_one({"username": username})
    return user_out


@router.post(
    "/", response_model=user_model.UserCreateOut, response_model_exclude_none=True
)
async def create_user(
    user_in: user_model.UserCreateIn = Body(...), db: MongoClient = Depends(db.get_db)
) -> Any:
    user = db.users.find_one(
        {"$or": [{"username": user_in.username}, {"email": user_in.email}]}
    )
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username or email already exists in the system.",
        )
    user_in.password = get_password_hash(user_in.password.get_secret_value())
    inserted_id = db.users.insert_one(user_in.dict()).inserted_id
    user = db.users.find_one({"_id": inserted_id})
    return user
