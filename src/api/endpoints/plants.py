from fastapi import APIRouter, Depends, HTTPException, Body, Path
from pymongo.mongo_client import MongoClient
import pymongo
import db
from models import plant as plant_model
import math
from endpoints.helpers_tools.db import prepare_search_query

router = APIRouter()


@router.get("/{science_name}", response_model=plant_model.Plant)
async def get_plant(
    science_name: str = Path(...), db: MongoClient = Depends(db.get_db)
):
    plant = db.plants.find_one({"science_name": science_name})
    if not plant:
        raise HTTPException(
            status_code=404,
            detail="plant not found",
        )
    return plant


@router.post("/search", response_model=plant_model.SearchOutList)
async def search(
    db: MongoClient = Depends(db.get_db),
    search: plant_model.SearchIn = Body(...),
):
    per_page = 30  # * limit to 30 per page
    query = prepare_search_query(search_input=search)
    count_documents = db.plants.count_documents(query)
    if count_documents == 0:
        return {}
    out_plants = plant_model.SearchOutList()
    out_plants.total_pages = math.floor(count_documents / per_page) + 1
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
