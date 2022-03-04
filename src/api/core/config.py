from pydantic import BaseSettings
import secrets
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "encyclo-flower API"
    API_PREFIX: str = "/api/v1"
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://root:example@localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "dev")

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # ! replace this with a secret key

    CLOUD_BUCKET: str = os.getenv(
        "CLOUD_BUCKET", "test1-ohad"
    )  # ! replace with "encyclo-flower". or env ?


# settings = Settings()
@lru_cache()
def get_settings():
    return Settings()
