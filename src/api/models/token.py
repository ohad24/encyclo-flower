from pydantic import BaseModel, Field
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    # * https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.6
    sub: str = Field(description="username")
    iat: float = Field(description="issued at, in seconds since epoch")
    exp: datetime = Field(description="expiration date")
