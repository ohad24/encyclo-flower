from fastapi import APIRouter, Depends, HTTPException, Form
from pymongo.mongo_client import MongoClient
import pymongo
from typing import Any, List, Dict
import db
from core.security import oauth2_scheme
from models import plant as plant_model
from pprint import pprint

router = APIRouter()


@router.get("/simple_search", response_model=plant_model.PlantsSearchOutList)
async def simple_search(
    db: MongoClient = Depends(db.get_db),
    token: str = Depends(oauth2_scheme),
    search: plant_model.SimplePlantsSearchIn = Depends(),
):
    # TODO: add from and limit as params - server side pagination
    print(search.name_text)
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
    out_plants = plant_model.PlantsSearchOutList(total=0, plants=[])
    if not query_and:
        return out_plants  # ! should return 400
    query = {"$and": query_and}
    pprint(query)
    per_page = 10  # * limit to 10
    total = db.plants.count_documents(query)
    print(total)
    if total == 0:
        return out_plants
    out_plants.total = total
    db_result = (
        db.plants.find(query)
        .sort([("science_name", pymongo.ASCENDING)])
        .skip(search.page * per_page)
        .limit(per_page)
    )
    print(db_result)
    plants = [plant for plant in db_result]
    print(len(plants))
    out_plants.plants = plants
    return out_plants
