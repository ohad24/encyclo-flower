from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
import db
from pymongo.mongo_client import MongoClient
from core.security import verify_password, create_access_token
from core.config import get_settings
from core.http_exceptions import e401
from models import token as token_schema
from models import user as user_model

settings = get_settings()

router = APIRouter()


@router.post("/token", response_model=token_schema.Token)
def login_for_access_token(
    db: MongoClient = Depends(db.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = db.users.find_one({"username": form_data.username})

    if not user:
        raise e401
    user = user_model.Login(**user)

    if not verify_password(form_data.password, user.password):
        raise e401

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.username, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# @router.post("/reset-password/", response_model=schemas.Msg)
# def reset_password(
#     token: str = Body(...),
#     new_password: str = Body(...),
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     """
#     Reset password
#     """
#     email = verify_password_reset_token(token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     user = crud.user.get_by_email(db, email=email)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     elif not crud.user.is_active(user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     hashed_password = get_password_hash(new_password)
#     user.hashed_password = hashed_password
#     db.add(user)
#     db.commit()
#     return {"msg": "Password updated successfully"}
