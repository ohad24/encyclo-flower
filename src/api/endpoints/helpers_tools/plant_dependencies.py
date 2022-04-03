from fastapi import HTTPException, status, Depends
from db import get_db
from pymongo.mongo_client import MongoClient
from models.plant import Plant, SearchIn, PreSearchData
from models.exceptions import (
    ExceptionPlantNotFound,
    ExceptionSearchPlantsNotFound,
    ExceptionSearchPageOutOfRange,
    ExceptionSearchNoInputCreteria,
)
from endpoints.helpers_tools.db import prepare_query_plant_name_text
from math import floor
from core.config import get_settings
from models.user import FavoritePlant

settings = get_settings()


async def get_plant_from_science_name(
    science_name: str,
    db: MongoClient = Depends(get_db),
) -> Plant:
    plant = db.plants.find_one({"science_name": science_name})
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ExceptionPlantNotFound().detail,
        )
    return Plant(**plant)


async def prepare_search_query(search_input: SearchIn) -> dict:
    """
    Set search query for DB.

    Created by @ofersadan85
    """
    query_and = (
        [prepare_query_plant_name_text(search_input.name_text)]
        if search_input.name_text
        else []
    )
    for field, value in search_input.dict(
        exclude_none=True, exclude_unset=True
    ).items():
        if field == "location_names":
            query_and += [
                {"locations.location_name": location_name} for location_name in value
            ]
        elif isinstance(value, list):
            query_and += [{field: {"$in": value}}]
        elif isinstance(value, bool):
            query_and += [{field: value}]

    if not query_and:
        raise HTTPException(
            status_code=400,
            detail=ExceptionSearchNoInputCreteria().detail,
        )
    query = {"$and": query_and}
    return query


async def get_pre_search_data(
    search_input: SearchIn,
    query: dict = Depends(prepare_search_query),
    db: MongoClient = Depends(get_db),
) -> PreSearchData:

    # * check if document exist
    documents_count = db.plants.count_documents(query)
    if documents_count == 0:
        raise HTTPException(
            status_code=404,
            detail=ExceptionSearchPlantsNotFound().detail,
        )

    # * check if page number is valid and not out of range
    total_pages = floor(documents_count / settings.ITEMS_PER_PAGE) + 1
    if search_input.page > total_pages:
        raise HTTPException(
            status_code=400,
            detail=ExceptionSearchPageOutOfRange().detail,
        )

    # * format return pre_search_data
    pre_search_data = PreSearchData(
        documents_count=documents_count,
        query=query,
        current_page=search_input.page,
        total_pages=total_pages,
        location_names=search_input.location_names,
    )
    return pre_search_data


async def get_favorite_plant_data(
    plant: Plant = Depends(get_plant_from_science_name),
) -> FavoritePlant:
    return FavoritePlant(**plant.dict())
