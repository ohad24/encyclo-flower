import db
from pymongo.mongo_client import MongoClient
from models.user import BaseUserIn, User
from fastapi import HTTPException, Depends
from core.security import get_current_active_user  # TODO: move this to here ?


async def validate_accept_terms_of_service(user_in: BaseUserIn):
    if not user_in.accept_terms_of_service:
        raise HTTPException(status_code=422, detail="Terms of service must be accepted")


async def validate_username_and_email_not_in_db(
    user_in: BaseUserIn, db: MongoClient = Depends(db.get_db)
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
    username: str, current_user: User = Depends(get_current_active_user)
):
    if current_user.username != username:
        raise HTTPException(
            status_code=400,
            detail="The user is not allowed to edit this user",
        )
