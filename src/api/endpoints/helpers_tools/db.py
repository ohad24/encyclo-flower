from fastapi import HTTPException


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


def prepare_search_query(search_input) -> dict:
    query_and = []
    if search_input.name_text:
        query_and.append(prepare_query_plant_name_text(search_input.name_text))
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
        query_or.append({"taxon.subfamily": {"$in": result_search_by_vision_api.labels}})
        query_or.append({"taxon.genus": {"$in": result_search_by_vision_api.labels}})
    from pprint import pprint
    pprint(query_or)
    return {"$or": query_or}
