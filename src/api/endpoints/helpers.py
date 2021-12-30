from fastapi import APIRouter, Query, HTTPException
from endpoints.helpers_tools.GPS_translate import find_point_location

from models import generic as generic_model
from models import plant as plant_model

router = APIRouter()


@router.get("/translate_gps", response_model=generic_model.GPSTranslateOut)
async def translate_gps(
    lat: float = Query(default=33.106251), lon: float = Query(default=35.719422)
):
    # TODO: remove default values
    # * test with https://www.latlong.net/
    # * tranlate location from GPS to location name using LocationKMLtranslate
    coords = (lon, lat)
    kml_location = find_point_location(coords)
    if not kml_location:
        raise HTTPException(
            status_code=404,
            detail="location not found",
        )
    return dict(location=plant_model.LocationKMLtranslate[kml_location].value)
