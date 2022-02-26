from pydantic import BaseModel


class ExceptionObservationNotFound(BaseModel):
    detail: str = "Observation not found1"


class ExceptionObservationImageNotFound(BaseModel):
    detail: str = "Image not found"


class ExceptionObservationImageCountLimit(BaseModel):
    detail: str = "10 images allowed per observation"
