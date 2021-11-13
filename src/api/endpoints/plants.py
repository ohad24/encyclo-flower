from fastapi import APIRouter, Depends, HTTPException, Body, Path
from pymongo.mongo_client import MongoClient
import pymongo
import db
from models import plant as plant_model
import math

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


def prepare_search_query(search_input) -> dict:
    query_and = []
    if search_input.name_text:
        nt = search_input.name_text
        name_text_or = [
            {"science_name": {"$regex": nt, "$options": "-i"}},
            {"heb_name": {"$regex": nt, "$options": "-i"}},
        ]
        for arr in ["arr_syn_name_eng", "arr_syn_name_heb"]:
            # * "in" not allow nestest $ in query
            name_text_or.append(
                {
                    arr: {
                        "$elemMatch": {
                            "$regex": nt,
                            "$options": "-i",
                        }
                    }
                }
            )
        query_and.append({"$or": name_text_or})
    if search_input.seasons:
        query_and.append({"season_num": {"$in": search_input.seasons}})
    if search_input.colors:
        query_and.append({"arr_color_name": {"$in": search_input.colors}})
    if search_input.location_names:
        for location_name in search_input.location_names:
            query_and.append({f"arr_location_name.{location_name}": {"$exists": True}})
    if search_input.petals:
        query_and.append({"petal_num_name": {"$in": search_input.petals}})
    if search_input.life_form:
        query_and.append({"life_form_name": {"$in": search_input.life_form}})
    if search_input.habitat:
        query_and.append({"arr_habitat_name": {"$in": search_input.habitat}})
    if search_input.stem_shape:
        stem_or = []
        for stem_shape in search_input.stem_shape:
            stem_or.append({"stem_shape_name": stem_shape})
        query_and.append({"$or": stem_or})
    if search_input.spine:
        query_and.append({"spine": {"$in": search_input.spine}})
    if search_input.red:
        query_and.append({"red": search_input.red})
    if search_input.invasive:
        query_and.append({"invasive": search_input.invasive})
    if search_input.danger:
        query_and.append({"denger": search_input.danger})
    if search_input.rare:
        query_and.append({"rare": search_input.rare})

    if not query_and:
        raise HTTPException(
            status_code=400,
            detail="must supply at least one parameter",
        )
    query = {"$and": query_and}
    return query


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
        .sort([("science_name", pymongo.ASCENDING)])
        .skip((search.page - 1) * per_page)
        .limit(per_page)
    )
    return out_plants
