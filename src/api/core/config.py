from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "encyclo-flower API"
    API_PREFIX: str = "/api/v1"
    MONGO_HOST: str = "localhost"
    MONGO_DB_NAME: str = "dev"
    MONGO_USERNAME: str = "root"
    MONGO_PASSWORD: str = "example"


settings = Settings()