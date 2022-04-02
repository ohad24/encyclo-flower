from fastapi import APIRouter, Depends
from pymongo.mongo_client import MongoClient
from db import get_db
from models.plant import Plant, SearchOutList, PreSearchData
from endpoints.helpers_tools.plant_dependencies import (
    get_plant_from_science_name,
    get_pre_search_data,
)
from endpoints.helpers_tools.generic import format_search_out_plant
from models.exceptions import (
    ExceptionPlantNotFound,
    ExceptionSearchPlantsNotFound,
    ExceptionSearchPageOutOfRange,
    ExceptionSearchNoInputCreteria,
)
from typing import Union

router = APIRouter()


@router.get(
    "/{science_name}",
    response_model=Plant,
    responses={
        404: {
            "description": ExceptionPlantNotFound().detail,
            "model": ExceptionPlantNotFound,
        }
    },
)
async def get_plant(
    plant: Plant = Depends(get_plant_from_science_name),
):
    return plant


@router.post(
    "/search",
    response_model=SearchOutList,
    responses={
        404: {
            "description": ExceptionSearchPlantsNotFound().detail,
            "model": ExceptionSearchPlantsNotFound,
        },
        400: {
            "description": "User input is not valid",
            "model": Union[
                ExceptionSearchNoInputCreteria, ExceptionSearchPageOutOfRange
            ],
        },
    },
)
async def search(
    pre_search_data: PreSearchData = Depends(get_pre_search_data),
    db: MongoClient = Depends(get_db),
):
    # * init return data
    out_plants = SearchOutList(
        total_pages=pre_search_data.total_pages,
        total=pre_search_data.documents_count,
        current_page=pre_search_data.current_page,
    )

    # * get plants from db
    plants = (
        db.plants.find(pre_search_data.query)
        .skip((pre_search_data.current_page - 1) * pre_search_data.per_page)
        .limit(pre_search_data.per_page)
    )

    # * format plants results
    out_plants.plants = [
        format_search_out_plant(Plant(**plant), pre_search_data.location_names)
        for plant in plants
    ]

    # * sort plants results
    out_plants.sort_plants()

    return out_plants
