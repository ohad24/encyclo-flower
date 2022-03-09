from google.cloud import storage
from core.config import get_settings
import os
from pathlib import Path


def check_google_credentials_file_exists() -> bool:
    """
    Check if the google credentials file exists.

    For skipping tests if the credentials file is not found.
    """
    google_credentials_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if google_credentials_file and Path(google_credentials_file).is_file():
        return True
    return False


if check_google_credentials_file_exists():
    settings = get_settings()
    storage_client = storage.Client()
    bucket = storage_client.bucket(settings.CLOUD_BUCKET)
else:
    bucket = None
