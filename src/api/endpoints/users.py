from fastapi import APIRouter, Depends
from typing import Any, List
from pymongo.mongo_client import MongoClient
import db
from schemas.user import User, UserInDBBase

router = APIRouter()




@router.get("/", response_model=List[User])
async def read_users(db: MongoClient = Depends(db.get_db)):
    users = [user for user in db.users.find({})]
    print(users)
    return users

# @router.get("/", response_model=List[schemas.User])
# def read_users(
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Retrieve users.
#     """
#     users = crud.user.get_multi(db, skip=skip, limit=limit)
#     return users