from pymongo import MongoClient
from core.config import get_settings

settings = get_settings()

db_client = MongoClient(
    host=settings.MONGO_HOST,
    port=27017,
    username=settings.MONGO_USERNAME,
    password=settings.MONGO_PASSWORD,
)


def get_db():
    # print(type(db_client))
    db_name = settings.MONGO_DB_NAME
    return db_client[db_name]
