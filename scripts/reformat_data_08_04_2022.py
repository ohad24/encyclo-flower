import json

"""
https://trello.com/c/Y74TfSZ7
"""


def fix_genus(plant):
    if plant["taxon"]["genus"] == "שיטה Faidherbia":
        plant["taxon"]["genus"] = "שיטה"
    return plant


def fix_family(plant):
    if (
        plant["taxon"]["family"] == "כליליים"
        or plant["taxon"]["family"] == "שיטיים"
        or plant["taxon"]["family"] == "פרפרניים"
        or plant["taxon"]["family"] == "קסאלפיניים"
    ):
        plant["taxon"]["family"] = "קטניות"
        plant["fam_name_heb"] = "קטניות"

        if "שיטה" in plant["taxon"]["genus"]:
            plant["taxon"]["subfamily"] = "מימוסיים \ שיטיים"
            plant["taxon"]["genus"] = "שיטה"

        elif (
            plant["taxon"]["genus"] == "כסיה"
            or plant["taxon"]["genus"] == "סנא"
            or plant["taxon"]["genus"] == "כליל"
            or plant["taxon"]["genus"] == "חרוב"
        ):
            plant["taxon"]["subfamily"] = "קסאלפיניים"

        else:
            plant["taxon"]["subfamily"] = "פרפרניים"
    return plant


def fix_color(plant):
    if "ארגמן" in plant["colors"]:
        plant["colors"].remove("ארגמן")

        if "בורדו" not in plant["colors"]:
            plant["colors"].append("בורדו")

    if "לילך" in plant["colors"]:
        if "ורוד" in plant["colors"] or "סגול" in plant["colors"]:
            plant["colors"].remove("לילך")

        else:
            plant["colors"].append("סגול")
            plant["colors"].append("ורוד")

    if "קרומי" in plant["colors"]:
        plant["colors"].remove("קרומי")
        if len(plant["colors"]) == 0:
            plant["colors"].append("קרם")
            plant["colors"].append("לבן")
        # print(plant["colors"])

    if "ללא עטיף" in plant["colors"]:
        plant["colors"].remove("ללא עטיף")
        plant["colors"].append("ללא עטיף - ללא עלי כותרת")
        print(plant["colors"])

    return plant


def fix_leaf_shape(plant):
    if "גזור פעם אחת" in plant["leaf_shapes"]:
        plant["leaf_shapes"].remove("גזור פעם אחת")
        plant["leaf_shapes"].append("גזור")
    if "מנוצה פעם אחת" in plant["leaf_shapes"]:
        plant["leaf_shapes"].remove("מנוצה פעם אחת")
        plant["leaf_shapes"].append("מנוצה")
    if "מנוצה פעם אחת או פעמיים" in plant["leaf_shapes"]:
        plant["leaf_shapes"].remove("מנוצה פעם אחת או פעמיים")
        plant["leaf_shapes"].append("מנוצה")
    if " תלתני" in plant["leaf_shapes"]:
        plant["leaf_shapes"].remove(" תלתני")
        plant["leaf_shapes"].append("תלתני")
    return plant


def update_fields(plant):
    plant = fix_genus(plant)
    plant = fix_family(plant)
    plant = fix_color(plant)
    plant = fix_leaf_shape(plant)
    return plant


if __name__ == "__main__":
    plants_data = json.load(open("scripts/plant_data_07_03_2022.json"))
    new_plants = list(map(update_fields, plants_data))

    json.dump(
        new_plants,
        open("scripts/plant_data_08_04_2022.json", "w"),
        default=str,
        indent=4,
        ensure_ascii=False,
    )
