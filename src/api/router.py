from fastapi import APIRouter
from endpoints import users, login, plants, helpers, detect


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(plants.router, prefix="/plants", tags=["plants"])
api_router.include_router(helpers.router, prefix="/helpers", tags=["helpers"])
api_router.include_router(detect.router, prefix="/detect", tags=["detect"])
