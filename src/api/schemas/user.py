from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic import BaseModel
from schemas.common import PyObjectId


# Shared properties
class UserBase(BaseModel):
    user: str
    name: str


class UserInDBBase(UserBase):
    _db_id: PyObjectId = Field(
        alias="_id", title="Mongo object id", default_factory=PyObjectId
    )

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# Additional properties to return via API
class User(UserInDBBase):
    pass


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
