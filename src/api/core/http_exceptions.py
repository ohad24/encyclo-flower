from fastapi import HTTPException, status

# TODO: move to models.exceptions

e403 = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="The user does not have enough privileges",
)
