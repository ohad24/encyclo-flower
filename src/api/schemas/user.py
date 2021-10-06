from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from schemas.common import PyObjectId
from typing import Optional


# Shared properties
class UserBase(BaseModel):
    username: str
    name: str
    email: Optional[EmailStr] = None


class UserInDBBase(UserBase):
    _db_id: PyObjectId = Field(
        alias="_id", title="Mongo object id", default_factory=PyObjectId
    )

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# Additional properties to return via API
class User(UserInDBBase):
    # password: str
    # _password: Optional[str] = Field(alias="password") # = PrivateAttr(Field("", title="Password"))
    pass

# Properties to receive via API on creation
class UserCreate(UserBase):
    # username: EmailStr
    password: str


class Login(BaseModel):
    username: str
    password: str

# # Shared properties
# class UserBase(BaseModel):
#     email: Optional[EmailStr] = None
#     is_active: Optional[bool] = True
#     is_superuser: bool = False
#     full_name: Optional[str] = None


# # Properties to receive via API on creation
# class UserCreate(UserBase):
#     email: EmailStr
#     password: str
