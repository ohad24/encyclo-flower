from fastapi import APIRouter, Depends
from fastapi.openapi.docs import get_swagger_ui_html
from core.security import validate_http_basic_cred

router = APIRouter()


@router.get("/")
def read_root():
    """For health check purposes."""
    return {"Hello": "World"}


@router.get(
    "/docs", include_in_schema=False, dependencies=[Depends(validate_http_basic_cred)]
)
async def get_swagger_documentation():
    """Set the /docs endpoint in /api/docs and secure it."""
    # * from https://github.com/tiangolo/fastapi/issues/364
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")
