import datetime
from PIL import Image
import io
from models.generic import AngleEnum


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


def rotate_image(image: bytes, angle: AngleEnum) -> bytes:
    bytes = io.BytesIO(image)
    image = Image.open(bytes)
    rotated = image.transpose(AngleEnum[angle].value)
    bytes = io.BytesIO()
    rotated.save(bytes, format=image.format)
    return bytes.getvalue()
