import json


"""
to replace

arr_syn_name_heb > synonym_names_heb
arr_syn_name_eng > synonym_names_eng
life_form_name > life_forms
arr_habitat_name > habitats
new class for leaf

leaf_shape_name > leaf_shapes
leaf_edge_name > leaf_edges
leaf_arrangement > leaf_arrangements

stem_shape_name > stem_shapes

petal_num_name > petal_num
arr_color_name > colors
season_num > flowering_seasons
arr_location_name > locations
locations with commoness - update shahar with solutions with translations

denger > danger
fam_name_eng - rename and add to others keys or taxons
add external sites and Organizem
"""

plants_data = json.load(open("scripts/plant_data_1_11_2021.json"))


def set_image(image: dict):
    image["what_inside"] = []
    image["image_date"] = None
    image["location"] = []
    image["general_description"] = image.pop("description")
    image["specific_description"] = None
    image["licenses"] = list(set(image["licenses"]))
    image["source_url"] = image.pop("image_url")
    image["source_url_page"] = image.pop("image_page_url")
    image["level"] = None
    image["file_name"] = image.pop("gen_file_name")
    return image


def set_taxon(taxon: dict):
    taxon["genus"] = taxon.get("genus", None)
    taxon["subfamily"] = taxon.get("subfamily", None)
    taxon["famely"] = taxon.get("famely", None)
    taxon["clade4"] = taxon.get("clade4", None)
    taxon["clade3"] = taxon.get("clade3", None)
    taxon["clade2"] = taxon.get("clade2", None)
    taxon["clade1"] = taxon.get("clade1", None)
    return taxon


def update_keys(plant: dict):
    plant["synonym_names_heb"] = plant.pop("arr_syn_name_heb")
    plant["synonym_names_eng"] = plant.pop("arr_syn_name_eng")
    plant["life_forms"] = plant.pop("life_form_name")
    plant["habitats"] = plant.pop("arr_habitat_name")
    plant["leaf_shapes"] = plant.pop("leaf_shape_name")
    plant["leaf_edges"] = plant.pop("leaf_edge_name")
    plant["leaf_arrangements"] = plant.pop("leaf_arrangement")
    plant["stem_shapes"] = plant.pop("stem_shape_name")
    plant["petal_num"] = plant.pop("petal_num_name")
    plant["colors"] = plant.pop("arr_color_name")
    plant["flowering_seasons"] = plant.pop("season_num")
    plant["locations"] = plant.pop("arr_location_name")
    plant["danger"] = plant.pop("denger")
    plant["taxon"] = set_taxon(plant["taxon"])
    plant["external_sites"] = []
    plant["organism"] = None
    plant['others'] = {}
    plant['others']["famely_eng"] = plant.pop("fam_name_eng")

    # * images handling
    if "images_data" in plant:
        plant["images"] = plant.pop("images_data")
        plant["images"] = {} if plant["images"] is None else plant["images"]
        plant["images"] = {"data": [set_image(image) for image in plant["images"]]}
    else:
        plant["images"] = None
    return plant


if __name__ == "__main__":
    new_plants_with_images = list(map(update_keys, plants_data))

    def separate_images(plant: dict):
        new_plant_images = {}
        if plant["images"]:
            new_plant_images["science_name"] = plant["science_name"]
            new_plant_images["data"] = plant["images"]["data"]
        plant.pop("images")
        return plant, new_plant_images

    new_plants, new_plants_images = zip(*map(separate_images, new_plants_with_images))

    json.dump(
        new_plants,
        open("scripts/plant_data_27_11_2021.json", "w"),
        default=str,
        indent=4,
        ensure_ascii=False,
    )

    json.dump(
        new_plants_images,
        open("scripts/plant_data_27_11_2021_images.json", "w"),
        default=str,
        indent=4,
        ensure_ascii=False,
    )
