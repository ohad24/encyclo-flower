import json
import string
import random

"""
remove typeo taxon.famely
add plant id to each plant
"""


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def update_plants(plant_data):
    # add plant id to each plant (with lowwer case letters and digits), 8 characters total
    plant_data["plant_id"] = id_generator()
    plant_data.get("taxon").pop("famely", None)
    return plant_data


if __name__ == "__main__":
    plants_data = json.load(open("scripts/plant_data_27_11_2021.json"))
    new_plants_with_images = list(map(update_plants, plants_data))

    # def separate_images(plant: dict):
    #     new_plant_images = {}
    #     if plant["images"]:
    #         new_plant_images["science_name"] = plant["science_name"]
    #         new_plant_images["data"] = plant["images"]["data"]
    #     plant.pop("images")
    #     return plant, new_plant_images

    # new_plants, new_plants_images = zip(*map(separate_images, new_plants_with_images))

    json.dump(
        new_plants_with_images,
        open("scripts/plant_data_31_01_2022.json", "w"),
        default=str,
        indent=4,
        ensure_ascii=False,
    )
