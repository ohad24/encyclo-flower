from pymongo import MongoClient
from core.config import settings

db_client = MongoClient(
        host=settings.MONGO_HOST,
        port=27017,
        username=settings.MONGO_USERNAME,
        password=settings.MONGO_PASSWORD,
    )


def get_db():
    # print(type(db_client))
    return db_client[settings.MONGO_DB_NAME]
