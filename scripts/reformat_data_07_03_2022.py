import json

"""
update one field. petal_num to petals
"""


def update_field(plant):
    plant["petals"] = plant["petal_num"]
    del plant["petal_num"]
    return plant


if __name__ == "__main__":
    plants_data = json.load(open("scripts/plant_data_17_02_2022.json"))
    new_plants_new_locations = list(map(update_field, plants_data))

    json.dump(
        new_plants_new_locations,
        open("scripts/plant_data_07_03_2022.json", "w"),
        default=str,
        indent=4,
        ensure_ascii=False,
    )
