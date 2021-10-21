from fastapi import APIRouter, Depends, HTTPException, Form
from typing import Any, List, Dict
from pymongo.mongo_client import MongoClient
import db
import models.user as user_model
from core.security import get_password_hash, oauth2_scheme, get_current_active_user

router = APIRouter()


@router.get("/", response_model=List[user_model.User])
async def read_users(
    db: MongoClient = Depends(db.get_db),
    current_user: user_model.User = Depends(get_current_active_user),
):
    users = list(db.users.find({}))
    # print(users)
    return users


@router.post("/", response_model=user_model.UserCreateOut)
async def create_user(
    *,
    db: MongoClient = Depends(db.get_db),
    user_in: user_model.UserCreateIn,
    # current_user: user_model.User = Depends(deps.get_current_active_superuser),
) -> Any:
    user = db.users.find_one({"username": user_in.username})
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user_in.password = get_password_hash(user_in.password)
    inserted_id = db.users.insert_one(user_in.dict()).inserted_id
    user = db.users.find_one({"_id": inserted_id})
    return user
