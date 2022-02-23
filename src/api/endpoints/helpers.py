from fastapi import APIRouter, Query
from models.generic import GPSTranslateOut
from endpoints.helpers_tools.generic import find_image_location

router = APIRouter()


@router.get("/translate_gps", response_model=GPSTranslateOut)
async def translate_gps(
    lat: float = Query(default=33.106251), lon: float = Query(default=35.719422)
):
    # TODO: remove default values
    # * test with https://www.latlong.net/
    # * tranlate location from GPS to location name using LocationKMLtranslate
    image_location = find_image_location(lon, lat, alt=0)
    return GPSTranslateOut(location=image_location.location_name)
