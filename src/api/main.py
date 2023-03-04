from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from router import api_router, base_router
from prometheus_fastapi_instrumentator import Instrumentator

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/openapi.json",
)

# TODO: update CORS after finish frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_main_router = APIRouter(prefix=settings.API_PREFIX)

api_main_router.include_router(
    api_router, prefix="/v1"
)  # TODO: set as variable from config (repo ?)
api_main_router.include_router(base_router)
app.include_router(api_main_router)

# * Prometheus metrics
Instrumentator().instrument(app).expose(app, include_in_schema=False)
