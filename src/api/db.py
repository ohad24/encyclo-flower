from pymongo import MongoClient
from pymongo.database import Database
from core.config import get_settings
from bson.codec_options import CodecOptions
import tzlocal

settings = get_settings()

db_client = MongoClient(settings.MONGO_URI)


def get_db() -> Database:
    # * https://pymongo.readthedocs.io/en/stable/examples/datetimes.html
    return db_client[settings.MONGO_DB_NAME].with_options(
        codec_options=CodecOptions(tz_aware=True, tzinfo=tzlocal.get_localzone())
    )
