from fastapi import HTTPException, status

# TODO: move to models.exceptions

e401 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password"
)

e403 = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="The user does not have enough privileges",
)
