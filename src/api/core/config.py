from pydantic import BaseSettings
import secrets


class Settings(BaseSettings):
    APP_NAME: str = "encyclo-flower API"
    API_PREFIX: str = "/api/v1"
    MONGO_HOST: str = "localhost"
    MONGO_DB_NAME: str = "dev"
    MONGO_USERNAME: str = "root"
    MONGO_PASSWORD: str = "example"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        60 * 24 * 8
    )  # 60 minutes * 24 hours * 8 days = 8 days
    SECRET_KEY: str = secrets.token_urlsafe(32)


settings = Settings()
