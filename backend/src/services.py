import json
import random
import uuid
from pathlib import Path
from typing import List

import pandas as pd
from fastapi import UploadFile
from fastapi.logger import logger

from schemas import DataPreview, Insight, UploadResponse
from utils import generate_file_id, get_insights_path, resolve_file_path, save_file


def process_upload(file: UploadFile) -> UploadResponse:
    """
    Helper function to save the uploaded file to the server and return a file preview

    Returns the file_id and the preview_data accroding to the UploadResposne Schema
    """
    try:
        file_path, file_id = save_uploaded_file(file)
        preview_data = extract_data_preview(file_path)
        return UploadResponse(file_id=file_id, preview=preview_data)
    except Exception as e:
        logger.error(f"[UploadError] Failed to process upload: {e}")
        raise


def save_uploaded_file(file: UploadFile) -> tuple[str, str]:
    """
    Save the uploaded file to the filesystem, and returns the first 5 rows
    """
    file_id = generate_file_id()
    try:
        # save the uploaded file
        file_path = save_file(file, file_id)
        return file_path, file_id
    except Exception as err:
        raise


def extract_data_preview(path: str, limit: int = 5) -> DataPreview:
    """
    Extract the first few rows of the file for preview.
    Returns a DataPreview schema object.
    """
    df = _read_dataframe(path)
    # preview_data = df.head(limit).to_dict(orient="records")
    preview_data = df.head(limit).fillna("").to_dict(orient="records")
    columns = df.columns.tolist()
    return DataPreview(columns=columns, rows=preview_data)


def generate_insights(file_id: str, count: int = 3) -> List[Insight]:
    """
    Simulate insights based on random sampling from the uploaded file.
    Returns a list of Insight schema objects.
    """
    file_path = resolve_file_path(file_id)

    if not file_path or not file_path.exists():
        raise FileNotFoundError(f"File not found for file ID: {file_id}")

    df = _read_dataframe(path)
    sampled = df.sample(min(count, len(df)))
    insights = []

    for idx, row in sampled.iterrows():
        insights.append(
            Insight(
                title=f"Insight on Row {idx}",
                description=f"This row contains something interesting worth noting.",
                confidence_score=round(random.uniform(0.7, 0.99), 2),
                reference_rows=[idx],
            )
        )

    return insights


def persist_insights(file_id: str, insights: List[Insight]) -> None:
    """
    Save generated insights to the filesystem in JSON format.
    """
    path = get_insights_path(file_id)
    try:
        with open(path, "w") as f:
            json.dump([insight.dict() for insight in insights], f)
    except Exception as e:
        logger.error(f"[PersistError] Could not save insights: {e}")
        raise


def retrieve_saved_insights(file_id: str) -> List[Insight]:
    """
    Load previously saved insights from the filesystem.
    Returns a list of Insight schema objects.
    """
    path = get_insights_path(file_id)
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return [Insight(**item) for item in data]
    except FileNotFoundError:
        raise FileNotFoundError(f"No saved insights for file ID: {file_id}")
    except Exception as e:
        logger.error(f"[RetrieveError] Could not load insights: {e}")
        raise


def _read_dataframe(path: str) -> pd.DataFrame:
    try:
        if path.endswith(".xlsx") or path.endswith(".xls"):
            return pd.read_excel(path)
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"[ReadError] Could not read file {path}: {e}")
        raise
