from pymongo import MongoClient
from core.config import get_settings

settings = get_settings()

db_client = MongoClient(settings.MONGO_URI)


def get_db():
    return db_client[settings.MONGO_DB_NAME]
