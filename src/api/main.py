from fastapi import FastAPI, APIRouter
from core.config import get_settings
from router import api_router, base_router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/openapi.json",
)

api_main_router = APIRouter(prefix=settings.API_PREFIX)

api_main_router.include_router(
    api_router, prefix="/v1"
)  # TODO: set as variable from config (repo ?)
api_main_router.include_router(base_router)
app.include_router(api_main_router)
