from fastapi import APIRouter, Depends, HTTPException, Body, Path
from pymongo.mongo_client import MongoClient
import pymongo
import db
from models import plant
from pprint import pprint
import math

router = APIRouter()


@router.get("/{science_name}", response_model=plant.Plant)
async def get_plant(
    science_name: str = Path(...), db: MongoClient = Depends(db.get_db)
):
    plant = db.plants.find_one({"science_name": science_name})
    # plants = list(collection.find())
    if not plant:
        raise HTTPException(
            status_code=404,
            detail="plant not found",
        )
    return plant


per_page = 30  # * limit to 30 per page


def prepare_simple_query(search_params):
    query_and = []
    if search_params.name_text:
        name_text_or = [
            {"science_name": {"$regex": search_params.name_text, "$options": "-i"}},
            {"heb_name": {"$regex": search_params.name_text, "$options": "-i"}},
        ]
        query_and.append({"$or": name_text_or})
    if search_params.season_num:
        query_and.append({"season_num": {"$in": [search_params.season_num]}})
    if search_params.color_name:
        query_and.append({"arr_color_name": {"$in": [search_params.color_name]}})
    if search_params.location_name:
        query_and.append(
            {f"arr_location_name.{search_params.location_name}": {"$exists": True}}
        )
    if not query_and:
        raise HTTPException(
            status_code=400,
            detail="must supply at least one parameter",
        )
    query = {"$and": query_and}
    # print(query)
    return query


def check_requested_page(page, count_documents):
    total_pages = math.floor(count_documents / per_page) + 1
    if page > total_pages:
        raise HTTPException(
            status_code=400,
            detail="page number out of range",
        )
    return total_pages


@router.post("/simple_search", response_model=plant.PlantsSearchOutList)
async def simple_search(
    db: MongoClient = Depends(db.get_db),
    search: plant.SimplePlantsSearchIn = Body(...),
):
    query = prepare_simple_query(search)
    count_documents = db.plants.count_documents(query)
    if count_documents == 0:
        return {}
    out_plants = plant.PlantsSearchOutList()
    out_plants.pages = check_requested_page(search.page, count_documents)
    out_plants.total = count_documents
    out_plants.current_page = search.page
    out_plants.plants = list(
        db.plants.find(query)
        .sort([("science_name", pymongo.ASCENDING)])
        .skip((search.page - 1) * per_page)
        .limit(per_page)
    )
    return out_plants


# def prepare_advanced_query(search_params):
#     query_and = []
#     if search_params.name_text:
#         name_text_or = [
#             {"science_name": {"$regex": search_params.name_text, "$options": "-i"}},
#             {"heb_name": {"$regex": search_params.name_text, "$options": "-i"}},
#         ]
#         query_and.append({"$or": name_text_or})
#     if search_params.color_name:
#         print([x.colors for x in search_params.color_name])
#         query_and.append({"arr_color_name": {"$in": [x.colors for x in search_params.color_name]}})
#     query = {"$and": query_and}
#     return query


# @router.post("/advanced_search", response_model=plant.PlantsSearchOutList)
# async def advanced_search(
#     db: MongoClient = Depends(db.get_db),
#     search: plant.AdvancedPlantsSearchIn = Body(...)
# ):
#     print(search)
#     query = prepare_advanced_query(search)
#     print(query)
#     count_documents = db.plants.count_documents(query)
#     print(count_documents)
#     return {}
#     # count_documents = db.plants.count_documents(query)
#     # out_plants = plant.PlantsSearchOutList()
#     # if count_documents == 0:
#     #     return out_plants
#     # out_plants.total = count_documents
#     # out_plants.current_page = search.page
#     # per_page = 30
