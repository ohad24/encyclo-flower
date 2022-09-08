def prepare_query_plant_name_text(name: str) -> dict:
    name_text_or = [
        {"science_name": {"$regex": name, "$options": "-i"}},
        {"heb_name": {"$regex": name, "$options": "-i"}},
    ]
    for arr in ["synonym_names_eng", "synonym_names_heb"]:
        # * "in" not allow nestest $ in query
        name_text_or.append(
            {
                arr: {
                    "$elemMatch": {
                        "$regex": name,
                        "$options": "-i",
                    }
                }
            }
        )
    return {"$or": name_text_or}


def prepare_query_detect_image(result_detect_api_response: list) -> list:
    # * prepare data for DB (or query)
    or_query = [
        {"science_name": x["class_name"]} for x in result_detect_api_response.json()
    ]
    pipeline = [
        {"$match": {"$or": or_query}},
        {
            "$project": {
                "_id": 0,
                "heb_name": 1,
                "science_name": 1,
                "images.file_name": 1,
                "images.level": 1,
            }
        },
        {
            "$project": {
                "heb_name": 1,
                "science_name": 1,
                "images": {"$slice": ["$images", 5]},
                # TODO: need to upgrade to mongo 6 https://www.mongodb.com/docs/manual/reference/operator/aggregation/sortArray/
                # TODO: PR #129 https://github.com/ohad24/encyclo-flower/issues/129
                # "result": {
                #     "$sortArray": {"input": "$images", "sortBy": {"images.level": 1}}
                # },
            }
        },
    ]
    return pipeline


def prepare_aggregate_pipeline_w_users(
    query_filter: dict, skip: int, limit: int
) -> list:
    """
    In use in preview_list, questions and observations

    The pipeline joins the user collection with main collection
    """
    # TODO: fix "project", it might not needed because of model output
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
