from fastapi import APIRouter, Depends, HTTPException
from pymongo.mongo_client import MongoClient
import pymongo
import db
from models import plant as plant_model
from pprint import pprint
import math

router = APIRouter()


@router.get("/simple_search", response_model=plant_model.PlantsSearchOutList)
async def simple_search(
    db: MongoClient = Depends(db.get_db),
    search: plant_model.SimplePlantsSearchIn = Depends(),
):
    query_and = []
    if search.name_text:
        name_text_or = []
        name_text_or.append(
            {"science_name": {"$regex": search.name_text, "$options": "-i"}}
        )
        name_text_or.append(
            {"heb_name": {"$regex": search.name_text, "$options": "-i"}}
        )
        query_and.append({"$or": name_text_or})
    if search.season_num:
        query_and.append({"season_num": {"$in": [search.season_num]}})
    if search.color_name:
        query_and.append({"arr_color_name": {"$in": [search.color_name]}})
    if search.location_name:
        query_and.append({"arr_location_name": {"$in": [search.location_name]}})
    if not query_and:
        raise HTTPException(
            status_code=400,
            detail="must supply at least one parameter",
        )
    query = {"$and": query_and}
    count_documents = db.plants.count_documents(query)
    out_plants = plant_model.PlantsSearchOutList()
    if count_documents == 0:
        return out_plants
    out_plants.total = count_documents
    out_plants.current_page = search.page
    per_page = 30  # * limit to 30 per page
    out_plants.pages = math.floor(count_documents / per_page) + 1
    if search.page > out_plants.pages:
        raise HTTPException(
            status_code=400,
            detail="page number out of range",
        )

    out_plants.plants = list(
        db.plants.find(query)
        .sort([("science_name", pymongo.ASCENDING)])
        .skip((search.page - 1) * per_page)
        .limit(per_page)
    )

    return out_plants
