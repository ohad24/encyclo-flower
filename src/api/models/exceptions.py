from pydantic import BaseModel
from fastapi import status


class DetailUserNotFound(BaseModel):
    detail: str = "User not found"


class ExceptionUserNotFound(DetailUserNotFound):
    status_code: int = status.HTTP_404_NOT_FOUND


class ExceptionUserNotAuthenticated(BaseModel):
    # * Can be merge with oauth2_scheme in security.py
    detail: str = "Not authenticated"


class ExceptionUserNotPrivilege(BaseModel):
    detail: str = "The user does not have enough privileges"


class ExceptionUserNotAllowToEditThisUser(BaseModel):
    detail: str = "The user is not allowed to edit this user"


class ExceptionUserNotAcceptTermsOfService(BaseModel):
    detail: str = "Terms of service must be accepted"


class ExceptionUserOrEmailAlreadyExists(BaseModel):
    detail: str = "The user with this username or email already exists in the system."


class ExceptionPasswordNotMatch(BaseModel):
    detail: str = "The passwords do not match"


class ExceptionLogin(BaseModel):
    detail: str = "Incorrect username or password"


class ExceptionObservationNotFound(BaseModel):
    detail: str = "Observation not found"


class ExceptionObservationImageNotFound(BaseModel):
    detail: str = "Image not found"


class ExceptionObservationImageCountLimit(BaseModel):
    detail: str = "Too many images. Only 10 images allowed per observation."
