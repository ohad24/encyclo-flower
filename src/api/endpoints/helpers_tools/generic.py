from datetime import datetime
from PIL import Image
import io
from models.generic import AngleEnum, ImageLocation
from typing import List, Tuple
from exif import Image as ExifImage
from endpoints.helpers_tools.GPS_translate import find_point_location
from models.plant import LocationKMLtranslate
from models.custom_types import HebMonths, HebMonthLiteral


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
    # * get first image to new image key
    user_obj["image"] = None
    if user_obj.get("images", None):
        user_obj["image"] = user_obj["images"][0]
    # * remove images key
    user_obj.pop("images", None)

    # * set username in top level keys
    user_obj["username"] = user_obj["user_data"][0]["username"]
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
    lon = 0
    lat = 0
    alt = 0
    image_heb_month_taken = None
    if exif.has_exif:
        if hasattr(exif, "gps_longitude") and hasattr(exif, "gps_latitude"):
            # * get coordinates
            lon = decimal_coords(exif.gps_longitude, exif.gps_longitude_ref)
            lat = decimal_coords(exif.gps_latitude, exif.gps_latitude_ref)
            alt = exif.gps_altitude

        if hasattr(exif, "datetime_original"):
            #  * get image date (Date taken)
            image_dt = datetime.strptime(exif.datetime_original, "%Y:%m:%d %H:%M:%S")
            image_heb_month_taken = HebMonths[image_dt.month - 1]
    return lon, lat, alt, image_heb_month_taken


def find_image_location(lon: float, lat: float, alt: float) -> ImageLocation:
    image_location = ImageLocation(coordinates=dict(lat=lat, lon=lon, alt=alt))
    kml_location = find_point_location((lon, lat))
    if kml_location:
        image_location.location_name = LocationKMLtranslate[kml_location].value
    return image_location


def get_image_metadata(image: bytes) -> Tuple[ImageLocation, HebMonthLiteral]:
    """
    Get image location (ImageLocation, name and coordinates)
    and month taken (in Hebrew) from exif data.
    """
    lon, lat, alt, image_heb_month_taken = get_image_exif_data(image)
    image_location = find_image_location(lon, lat, alt)
    return image_location, image_heb_month_taken
