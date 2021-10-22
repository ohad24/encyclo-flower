from pymongo import MongoClient
from core.config import get_settings
import os

settings = get_settings()

db_client = MongoClient(
    f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}:{settings.MONGO_PORT}"
)


def get_db():
    db_name = os.getenv("MONGO_DB_NAME", settings.MONGO_DB_NAME)
    return db_client[db_name]
