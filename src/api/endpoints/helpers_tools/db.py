from fastapi import HTTPException
from models.plant import SearchIn


def prepare_query_plant_name_text(name_text):
    nt = name_text
    name_text_or = [
        {"science_name": {"$regex": nt, "$options": "-i"}},
        {"heb_name": {"$regex": nt, "$options": "-i"}},
    ]
    for arr in ["synonym_names_eng", "synonym_names_heb"]:
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
    return {"$or": name_text_or}


def prepare_search_query(search_input: SearchIn) -> dict:
    query_and = [prepare_query_plant_name_text(search_input.name_text)] if search_input.name_text else []
    for field, value in search_input.dict(exclude_none=True, exclude_unset=True).items():
        if field == 'location_names':
            query_and += [{"locations.location_name": location_name} for location_name in value]
        elif isinstance(value, list):
            query_and += [{field: {'$in': value}}]
        elif isinstance(value, bool):
            query_and += [{field: value}]

    if not query_and:
        raise HTTPException(
            status_code=400,
            detail="must supply at least one parameter",
        )
    query = {"$and": query_and}
    return query


def prepare_query_detect_image(
    result_google_search_by_image, result_search_by_vision_api
) -> dict:
    # * search in db
    query_or = []

    if result_google_search_by_image.kb_panel.scientific_name:
        # * kb.scientific_name > db.plants.science_name
        query_scientific_name = prepare_query_plant_name_text(
            result_google_search_by_image.kb_panel.scientific_name
        )
        query_or.append(query_scientific_name)

        # * kb.scientific_name (first word) > science_name (beginning of the word)
        query_first_world = prepare_query_plant_name_text(
            result_google_search_by_image.kb_panel.scientific_name.split(" ")[0]
        )
        query_or.append(query_first_world)

    if result_google_search_by_image.kb_panel.higher_classification:
        # * kb.higher_classification > db.plants.taxon.family
        # TODO: need to be stranslate to heb
        query_higher_classification = {
            "taxon.family": result_google_search_by_image.kb_panel.higher_classification
        }
        query_or.append(query_higher_classification)

    if result_google_search_by_image.kb_panel.family:
        # * kb.family > db.plants.taxon.family
        # TODO: need to be stranslate to heb
        query_family = {"taxon.family": result_google_search_by_image.kb_panel.family}
        query_or.append(query_family)

    if result_search_by_vision_api.labels:
        # * vision.labels > taxon.family/subfamily/genus
        # TODO: need to be stranslate to heb
        # TODO: need to filter words like "family"
        query_or.append({"taxon.family": {"$in": result_search_by_vision_api.labels}})
        query_or.append(
            {"taxon.subfamily": {"$in": result_search_by_vision_api.labels}}
        )
        query_or.append({"taxon.genus": {"$in": result_search_by_vision_api.labels}})
    from pprint import pprint

    pprint(query_or)
    return {"$or": query_or}


def prepare_aggregate_pipeline_w_users(
    query_filter: dict, skip: int, limit: int
) -> list:
    """
    In use in preview_list, questions and observations

    The pipeline joins the user collection with main collection
    """
    aggregate_pipeline = [
        {"$match": query_filter},
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "user_id",
                "as": "user_data",
            }
        },
        {
            "$project": {
                "_id": 0,
                "user_data.password": 0,
                "user_data._id": 0,
                "comments": 0,
            }
        },
        {"$sort": {"created_dt": -1}},
        {"$skip": skip},
        {"$limit": limit},
    ]
    return aggregate_pipeline


def prepare_aggregate_pipeline_comments_w_users(
    query_filter: dict, skip: int, limit: int
) -> list:
    """
    In use in get comments, questions and observations

    The pipeline joins the user collection with main collection
    """
    aggregate_pipeline = [
        {"$match": query_filter},
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "user_id",
                "as": "user_data",
            }
        },
        {"$unwind": "$user_data"},
        {
            "$project": {
                "comment_id": 1,
                "comment_text": 1,
                "create_dt": 1,
                "user_data.f_name": 1,
                "user_data.l_name": 1,
                "user_data.username": 1,
                "user_data.user_id": 1,
                "_id": 0,
            }
        },
        {"$sort": {"created_dt": -1}},
        {"$skip": skip},
        {"$limit": limit},
    ]
    return aggregate_pipeline
