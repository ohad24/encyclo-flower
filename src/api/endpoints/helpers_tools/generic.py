from datetime import datetime
from PIL import Image
import io
from models.generic import AngleEnum
from typing import List
from exif import Image as ExifImage


def get_today_str() -> str:
    return datetime.utcnow().strftime("%Y%m%d")


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


def get_first_uploaded_image(images: List[dict]) -> dict | None:
    # * get only uploaded images
    for img in images:
        if img.get("uploaded", None):
            return img
    return None


def format_obj_image_preview(user_obj: dict) -> dict:
    """user_obj is question or observation in dict type"""
    # * get only first image to new image key
    user_obj["image"] = get_first_uploaded_image(user_obj["images"])
    # * remove images key
    user_obj.pop("images", None)
    return user_obj


def decimal_coords(coords: tuple, ref: str) -> float:
    """
    convert gps coordinates tuple (degrees, minutes, seconds) + ref str (N,S,E,W) to decimal
    """
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def get_image_exif_data(image: bytes) -> tuple:
    """return tuple with lon, lat, alt and image_dt"""
    exif = ExifImage(image)
    lon = None
    lat = None
    alt = None
    image_dt = None
    if exif.has_exif:
        # * get coordinates
        lon = decimal_coords(exif.gps_longitude, exif.gps_longitude_ref)
        lat = decimal_coords(exif.gps_latitude, exif.gps_latitude_ref)
        alt = exif.gps_altitude

        #  * get image date (Date taken)
        image_dt = datetime.strptime(exif.datetime_original, "%Y:%m:%d %H:%M:%S")
    return lon, lat, alt, image_dt
