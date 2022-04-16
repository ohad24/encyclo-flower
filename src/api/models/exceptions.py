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


class ExceptionUserResetPasswordTokenNotFound(BaseModel):
    detail: str = "Reset password token not found"


class ExceptionEmailVerificationTokenNotFound(BaseModel):
    detail: str = "Email verification token not found"


class ExceptionLogin(BaseModel):
    detail: str = "Incorrect username or password"


class ExceptionObservationNotFound(BaseModel):
    detail: str = "Observation not found"


class ExceptionObservationImageNotFound(BaseModel):
    detail: str = "Image not found"


class ExceptionObservationImageCountLimit(BaseModel):
    detail: str = "Too many images. Only 10 images allowed per observation."


class ExceptionPlantNotFound(BaseModel):
    detail: str = "Plant not found."


class ExceptionSearchPlantsNotFound(BaseModel):
    detail: str = "No plants found."


class ExceptionSearchPageOutOfRange(BaseModel):
    detail: str = "Page number out of range."


class ExceptionSearchNoInputCreteria(BaseModel):
    detail: str = "Must supply at least one criteria for search."


class ExceptionPlantFavoriteAlreadyExists(BaseModel):
    detail: str = "Plant is already in favorites."


class ExceptionPlantFavoriteNotFound(BaseModel):
    detail: str = "Plant is not in favorites."


class ExceptionQuestionImageCountLimit(BaseModel):
    detail: str = "Too many images. Only 10 images allowed per question."
