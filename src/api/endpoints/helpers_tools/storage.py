from core.gstorage import bucket
from pathlib import Path


def upload_to_gstorage(
    file_name: str, dir_path: Path, image_bytes: bytes, content_type: str
):
    blob = bucket.blob(str(dir_path / file_name))
    blob.upload_from_string(image_bytes, content_type=content_type)
