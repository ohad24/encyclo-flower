import db
from pymongo.mongo_client import MongoClient
from models.user import BaseUserIn
from fastapi import HTTPException, Depends


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
