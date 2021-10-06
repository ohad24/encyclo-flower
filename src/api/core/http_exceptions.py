from fastapi import HTTPException, status
from pydantic import BaseModel

e401 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password"
)
