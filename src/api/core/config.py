from pydantic import BaseSettings, EmailStr
import secrets
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):

    # * Application settings
    APP_NAME: str = "encyclo-flower API"
    API_PREFIX: str = "/api"
    API_VERSION: str = "0.0.0"  # TODO: set as variable

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))

    # * Database settings
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "dev")

    # * Google bucket settings
    CLOUD_BUCKET: str = os.getenv("CLOUD_BUCKET")

    # * Email settings
    # * SMTP_USER and SMTP_PASS should be in environment variables
    EMAIL_ADDRESS: EmailStr = "encyclo.flower@gmail.com"
    EMAIL_VERIFICATION_EXPIRES_MINUTES: int = 60 * 24 * 2  # 2 days
    EMAIL_PASSWORD_RESET_EXPIRES_MINUTES: int = 60 * 24  # 1 days

    # * Search plant
    ITEMS_PER_PAGE: int = 30

    # * Plant detection
    DETECT_API_SRV = os.environ.get("DETECT_API_SRV", "http://localhost:5001/detect/")


@lru_cache()
def get_settings():
    return Settings()
