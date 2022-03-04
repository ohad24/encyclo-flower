from core.gstorage import bucket
from pathlib import Path
from typing import Tuple


def upload_to_gstorage(
    file_name: str, dir_path: Path, image_bytes: bytes, content_type: str
):
    blob = bucket.blob(str(dir_path / file_name))
    blob.upload_from_string(image_bytes, content_type=content_type)


def delete_from_gstorage(file_name: str, dir_path: Path):
    blob = bucket.blob(str(dir_path / file_name))
    blob.delete()


def download_from_gstorage(file_name: str, dir_path: Path) -> Tuple[bytes, str]:
    blob = bucket.blob(str(dir_path / file_name))
    return blob.download_as_bytes(), blob.content_type
