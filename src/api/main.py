from fastapi import FastAPI
from core.config import get_settings
from router import api_router

settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")  # ! NEED TO REMOVE
def read_root():
    return {"Hello": "World"}
