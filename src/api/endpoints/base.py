from os import environ
from fastapi import APIRouter, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from core.security import validate_http_basic_cred
from datetime import datetime
from core.config import get_settings

settings = get_settings()

router = APIRouter()


@router.get("/")
def read_root():
    """Basic check,
    For health check use api/health"""
    return {"Hello": "World"}


@router.get(
    "/docs", include_in_schema=False, dependencies=[Depends(validate_http_basic_cred)]
)
async def get_swagger_documentation():
    """Set the /docs endpoint in /api/docs and secure it."""
    # * from https://github.com/tiangolo/fastapi/issues/364
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")


@router.get("/health")
def read_health():
    """Check mandatory environment variables, server time,
    version, deployment environment ,etc."""

    def check_env_var(var_name):
        if var_name not in environ:
            return False
        return True

    # * check mandatory environment variables
    environment_variables = dict(
        CLOUD_BUCKET=check_env_var("CLOUD_BUCKET"),
        MONGO_URI=check_env_var("MONGO_URI"),
        GOOGLE_APPLICATION_CREDENTIALS=check_env_var("GOOGLE_APPLICATION_CREDENTIALS"),
    )

    # * check server time
    dt = datetime.now().astimezone()

    # * deployment environment (dev, test, prod)
    # TODO: set as variable
    deployment_environment = None

    # * api version
    api_version = settings.API_VERSION
    return dict(
        environment_variables=environment_variables,
        server_time=dt,
        deployment_environment=deployment_environment,
        api_version=api_version,
    )
