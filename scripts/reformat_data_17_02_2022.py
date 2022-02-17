import json
import string
import random

"""
refactor locations names and location commoness
"""

heb_trans = {
    "galilee coast": "חוף הגליל",
    "carmel coast": "חוף הכרמל",
    "sharon": "שרון",
    "southern coast": "מישור החוף הדרומי",
    "upper galilee": "גליל עליון",
    "lower galilee": "גליל תחתון",
    "carmel": "כרמל",
    "menashe hights": "רמות מנשה",
    "izrael valley": "עמק יזרעאל",
    "samarian mountains": "הרי שומרון",
    "shfela": "שפלת יהודה",
    "judaean mountains": "הרי יהודה",
    "north negev": "צפון הנגב",
    "west negev": "מערב הנגב",
    "central negev": "מרכז והר הנגב",
    "south negev": "דרום הנגב",
    "hula valley": "עמק החולה",
    "kinarot valley": "בקעת כינרות",
    "bit shean valley": "עמק בית שאן",
    "gilboa": "גלבוע",
    "shomron desert": "מדבר שומרון",
    "judaean desert": "מדבר יהודה",
    "jorden valley": "בקעת הירדן",
    "dead sea valley": "בקעת ים המלח",
    "arava": "ערבה",
    "hermon": "חרמון",
    "golan": "גולן",
    "gilad": "גלעד",
    "amon": "עמון",
    "moav": "מואב",
    "edom": "אדום",
}


def update_locations(plant):
    locations = []
    for location_name_eng, commoness in plant["locations"].items():
        location_name_heb = heb_trans[location_name_eng]
        d = {"location_name": location_name_heb, "commoness": commoness}
        locations.append(d)
    plant["locations"] = locations
    return plant


if __name__ == "__main__":
    plants_data = json.load(open("scripts/plant_data_31_01_2022.json"))
    new_plants_new_locations = list(map(update_locations, plants_data))

    json.dump(
        new_plants_new_locations,
        open("scripts/plant_data_17_02_2022.json", "w"),
        default=str,
        indent=4,
        ensure_ascii=False,
    )
