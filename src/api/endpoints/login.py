from datetime import timedelta
from fastapi import APIRouter, Depends
from core.security import create_access_token, get_user_for_login
from core.config import get_settings
from models.token import Token
from models.user import UserInDB
from models.exceptions import ExceptionLogin

settings = get_settings()

router = APIRouter()


@router.post(
    "/token",
    response_model=Token,
    summary="Login",
    description="Login using username and password",
    responses={
        401: {"description": ExceptionLogin().detail, "model": ExceptionLogin},
    },
)
def login_for_access_token(
    user: UserInDB = Depends(get_user_for_login),
) -> Token:
    access_token = create_access_token(
        user.username,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token)


# TODO: activate reset password
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
