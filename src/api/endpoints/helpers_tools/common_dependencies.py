from pydantic import BaseModel
from fastapi import Query


class QuerySearchPageParams(BaseModel):
    """
    From https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/#classes-as-dependencies_1
    """
    skip: int = Query(0, ge=0)
    limit: int = Query(9, ge=1, le=9)
