from pydantic import BaseModel
from fastapi import status


class DetailUserNotFound(BaseModel):
    detail: str = "User not found"


class ExceptionUserNotFound(DetailUserNotFound):
    status_code: int = status.HTTP_404_NOT_FOUND


class ExceptionLogin(BaseModel):
    detail: str = "Incorrect username or password"


class ExceptionObservationNotFound(BaseModel):
    detail: str = "Observation not found"


class ExceptionObservationImageNotFound(BaseModel):
    detail: str = "Image not found"


class ExceptionObservationImageCountLimit(BaseModel):
    detail: str = "Too many images. Only 10 images allowed per observation."
