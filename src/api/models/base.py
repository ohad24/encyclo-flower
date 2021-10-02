from pydantic import BaseModel, PrivateAttr, Field, schema
from bson import ObjectId
from bson.decimal128 import Decimal128
from datetime import datetime

class DBBaseModel(BaseModel):
    # * https://pydantic-docs.helpmanual.io/usage/model_config/#change-behaviour-globally

    _db_id: ObjectId = PrivateAttr(Field(alias="_id", title="Mongo object id"))
    # create_date: datetime = Field(
    #     default_factory=datetime.utcnow, hidden_from_schema=True, title="Creation date"
    # )

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, Decimal128: str}