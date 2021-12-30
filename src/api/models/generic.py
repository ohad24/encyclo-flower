from pydantic import BaseModel


class GPSTranslateOut(BaseModel):
    location: str
