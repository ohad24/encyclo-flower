from fastapi import APIRouter, Depends
from pymongo.mongo_client import MongoClient
from db import get_db
from models.plant import Plant, SearchOutList, PreSearchData
from endpoints.helpers_tools.plant_dependencies import (
    get_plant_from_science_name,
    get_pre_search_data,
)

router = APIRouter()


@router.get("/{science_name}", response_model=Plant)
async def get_plant(
    plant: Plant = Depends(get_plant_from_science_name),
):
    # TODO: add more response description
    return plant


@router.post("/search", response_model=SearchOutList)
async def search(
    pre_search_data: PreSearchData = Depends(get_pre_search_data),
    db: MongoClient = Depends(get_db),
):
    # TODO: add more response description
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
    out_plants.plants = [Plant(**plant) for plant in plants]

    return out_plants
