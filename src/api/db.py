from pymongo import MongoClient
from pymongo.database import Database
from core.config import get_settings
from bson.codec_options import CodecOptions
import tzlocal
import logging

logger = logging.getLogger("uvicorn")

settings = get_settings()

db_client = MongoClient(settings.MONGO_URI)
db_version = db_client.server_info()["version"]
logger.info(f"{db_version=}")


def get_db() -> Database:
    # * https://pymongo.readthedocs.io/en/stable/examples/datetimes.html
    return db_client[settings.MONGO_DB_NAME].with_options(
        codec_options=CodecOptions(tz_aware=True, tzinfo=tzlocal.get_localzone())
    )
