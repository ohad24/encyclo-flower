from pydantic import BaseModel, PrivateAttr, Field, schema
from bson import ObjectId
from bson.decimal128 import Decimal128
from datetime import datetime
from bson import ObjectId

class DBBaseModel(BaseModel):
    # * https://pydantic-docs.helpmanual.io/usage/model_config/#change-behaviour-globally

    _db_id: ObjectId = PrivateAttr(Field(alias="_id", title="Mongo object id"))
    # create_date: datetime = Field(
    #     default_factory=datetime.utcnow, hidden_from_schema=True, title="Creation date"
    # )

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, Decimal128: str}


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")