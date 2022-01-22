import datetime
import uuid


def get_today_str() -> str:
    return datetime.datetime.utcnow().strftime("%Y%m%d")


# * filter generic result in external apis
detect_image_blacklist = [
    "Flower",
    "Plant",
    "Grass",
    "Groundcover",
    "Flowering plant",
    "Terrestrial plant" "Shrub",
    "Herbaceous plant",
    "Subshrub" "Twig",
    "Evergreen",
    "Woody plant",
    "Tree",
    "Vascular plant",
    "Plant stem" "Petal",
    "Fruit",
    "Sky",
    "Plant community",
    "Cloud",
    "Natural environment",
    "Natural landscape",
    "Agriculture",
    "Grassland",
    "Close-up",
    "Photography",
    "Macro photography",
    "Spring",
    "Leaf",
    "Garden",
    "Wildflower",
    "YouTube",
    "Flowerpot",
    "Pedicel",
    "Flora",
]


def gen_image_file_name(file_name: str) -> str:
    return str(uuid.uuid4()) + "." + file_name.split(".")[-1]
