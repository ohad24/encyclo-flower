from google.cloud import storage
from core.config import get_settings

settings = get_settings()

storage_client = storage.Client()
bucket = storage_client.bucket(settings.CLOUD_BUCKET)
