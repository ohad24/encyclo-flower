from fastapi import HTTPException


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
    if search_input.flowering_seasons:
        query_and.append({"flowering_seasons": {"$in": search_input.flowering_seasons}})
    if search_input.colors:
        query_and.append({"colors": {"$in": search_input.colors}})
    if search_input.location_names:
        for location_name in search_input.location_names:
            query_and.append({f"locations.{location_name}": {"$exists": True}})
    if search_input.petals:
        query_and.append({"petal_num": {"$in": search_input.petals}})
    if search_input.life_forms:
        query_and.append({"life_forms": {"$in": search_input.life_forms}})
    if search_input.habitats:
        query_and.append({"habitats": {"$in": search_input.habitats}})
    if search_input.stem_shapes:
        query_and.append({"stem_shapes": {"$in": search_input.stem_shapes}})
    if search_input.spine:
        query_and.append({"spine": {"$in": search_input.spine}})
    if search_input.red:
        query_and.append({"red": search_input.red})
    if search_input.invasive:
        query_and.append({"invasive": search_input.invasive})
    if search_input.danger:
        query_and.append({"danger": search_input.danger})
    if search_input.rare:
        query_and.append({"rare": search_input.rare})

    if not query_and:
        raise HTTPException(
            status_code=400,
            detail="must supply at least one parameter",
        )
    query = {"$and": query_and}
    return query
