from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from pymongo.mongo_client import MongoClient
from db import get_db
from models.plant import Plant, SearchOutList, PreSearchData, PlantAutoCompleteOut
from endpoints.helpers_tools.plant_dependencies import (
    get_plant_from_science_name,
    get_pre_search_data,
    get_favorite_plant_data,
)
from endpoints.helpers_tools.generic import format_search_out_plant
from models.exceptions import (
    ExceptionPlantNotFound,
    ExceptionSearchPlantsNotFound,
    ExceptionSearchPageOutOfRange,
    ExceptionSearchNoInputCreteria,
    ExceptionPlantFavoriteAlreadyExists,
    ExceptionPlantFavoriteNotFound,
)
from typing import Union, List
from core.security import get_current_active_user
from models.user import UserInDB, FavoritePlant
from endpoints.helpers_tools.db import prepare_query_plant_name_text

router = APIRouter()


@router.get(
    "/autocomplete",
    response_model=List[PlantAutoCompleteOut],
    summary="Autocomplete plants name",
    description="Autocomplete plants name, mainly for UI fields. Limit to 20 results",
)
async def autocomplete(
    search_input: str = Query("", min_length=2),
    db: MongoClient = Depends(get_db),
):
    query = prepare_query_plant_name_text(search_input)
    plants = [
        PlantAutoCompleteOut(**plant) for plant in db.plants.find(query).limit(20)
    ]
    return plants


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


@router.put(
    "/{science_name}/add-favorite",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        "400": {
            "description": ExceptionPlantFavoriteAlreadyExists().detail,
            "model": ExceptionPlantFavoriteAlreadyExists,
        },
        404: {
            "description": ExceptionPlantNotFound().detail,
            "model": ExceptionPlantNotFound,
        },
    },
)
async def add_favorite(
    current_user: UserInDB = Depends(get_current_active_user),
    favorite_plant: FavoritePlant = Depends(get_favorite_plant_data),
    db: MongoClient = Depends(get_db),
):
    result = db.users.update_one(
        {"user_id": current_user.user_id},
        {"$addToSet": {"favorite_plants": favorite_plant.dict()}},
    )
    if not result.modified_count:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ExceptionPlantFavoriteAlreadyExists().detail,
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{science_name}/remove-favorite",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        "400": {
            "description": ExceptionPlantFavoriteNotFound().detail,
            "model": ExceptionPlantFavoriteNotFound,
        },
        404: {
            "description": ExceptionPlantNotFound().detail,
            "model": ExceptionPlantNotFound,
        },
    },
)
async def remove_favorite(
    current_user: UserInDB = Depends(get_current_active_user),
    favorite_plant: FavoritePlant = Depends(get_favorite_plant_data),
    db: MongoClient = Depends(get_db),
):
    result = db.users.update_one(
        {"user_id": current_user.user_id},
        {"$pull": {"favorite_plants": favorite_plant.dict()}},
    )
    if not result.modified_count:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ExceptionPlantFavoriteNotFound().detail,
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
