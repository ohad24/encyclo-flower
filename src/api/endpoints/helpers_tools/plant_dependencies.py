from fastapi import HTTPException, status, Depends
from db import get_db
from pymongo.mongo_client import MongoClient
from models.plant import Plant
from models.exceptions import ExceptionPlantNotFound


async def get_plant_from_science_name(
    science_name: str,
    db: MongoClient = Depends(get_db),
) -> Plant:
    plant = db.plants.find_one({"science_name": science_name})
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ExceptionPlantNotFound().detail,
        )
    return Plant(**plant)
