from fastapi import APIRouter, Depends, HTTPException, Body
from pymongo.mongo_client import MongoClient
from db import get_db
from models.plant import Plant, SearchOutList, SearchIn
from math import floor
from endpoints.helpers_tools.db import prepare_search_query
from endpoints.helpers_tools.plant_dependencies import get_plant_from_science_name

router = APIRouter()


@router.get("/{science_name}", response_model=Plant)
async def get_plant(
    plant: Plant = Depends(get_plant_from_science_name),
):
    return plant


@router.post("/search", response_model=SearchOutList)
async def search(
    db: MongoClient = Depends(get_db),
    search: SearchIn = Body(...),
):
    per_page = 30  # * limit to 30 per page
    query = prepare_search_query(search_input=search)
    count_documents = db.plants.count_documents(query)
    if count_documents == 0:
        return {}
    out_plants = SearchOutList()
    out_plants.total_pages = floor(count_documents / per_page) + 1
    if search.page > out_plants.total_pages:
        raise HTTPException(
            status_code=400,
            detail="page number out of range",
        )
    out_plants.total = count_documents
    out_plants.current_page = search.page
    out_plants.plants = list(
        db.plants.find(query)
        # .sort([("images", pymongo.ASCENDING)])  # * FIX THIS
        .skip((search.page - 1) * per_page).limit(per_page)
    )
    return out_plants
