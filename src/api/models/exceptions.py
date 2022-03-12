from pydantic import BaseModel


class ExceptionLogin(BaseModel):
    detail: str = "Incorrect username or password"


class ExceptionObservationNotFound(BaseModel):
    detail: str = "Observation not found"


class ExceptionObservationImageNotFound(BaseModel):
    detail: str = "Image not found"


class ExceptionObservationImageCountLimit(BaseModel):
    detail: str = "Too many images. Only 10 images allowed per observation."
