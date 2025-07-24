import os
import random
import uuid
from pathlib import Path

from fastapi import UploadFile

BASE_PATH = Path(__file__).resolve().parent
MEDIA_DIR = BASE_PATH / "mediafiles"
UPLOAD_DIR = BASE_PATH / "uploads"
INSIGHT_DIR = BASE_PATH / "insights"

for directory in (MEDIA_DIR, UPLOAD_DIR, INSIGHT_DIR):
    directory.mkdir(parents=True, exist_ok=True)


def generate_file_id() -> str:
    """Generate a unique file ID."""
    # converts the UUID to a string, converting the hypens to underscores
    # and returns it
    return str(uuid.uuid4()).replace("-", "_")


def resolve_file_path(file_id: str, ext: str = "xlsx") -> str:
    """Resolve the file path for a given file ID."""
    return os.path.join(MEDIA_DIR, f"{file_id}.{ext}")


def get_insights_path(file_id: str) -> str:
    """
    Get the path for storing or retrieving insights for a given file ID.
    """
    return str(INSIGHT_DIR / f"{file_id}.json")


def save_file(file: UploadFile, file_id: str):
    ext = file.filename.split(".")[-1]
    path = resolve_file_path(file_id, ext)

    with open(path, "wb") as f:
        f.write(file.file.read())
    return path


def generate_insights(file_id: str):
    """
    Simulate insight generation for a file.

    - Make call to our MCP server
    - Return resposne to generate_insights_data service function call
    """
    # Placeholder logic for actual OpenRouter call or mock generation
    pass
