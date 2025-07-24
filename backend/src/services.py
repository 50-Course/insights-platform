import json
import os
import random
import uuid
from pathlib import Path
from typing import List, Optional

import pandas as pd
from fastapi import UploadFile
from fastapi.logger import logger

from exceptions import (
    FileNotFoundException,
    FileProcessingError,
    InsightsNotFoundException,
)
from mcp_client import generate_ai_insights
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
        raise FileProcessingError(
            "An error occurred while processing the file",
            details={"error": str(e)},
        ) from e


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
    ext = os.path.splitext(path)[1].lower()

    if ext in {".csv", ".xlsx", ".xls"}:
        df = _read_dataframe(path)
    elif ext in {".txt", ".docx"}:
        lines = read_word_text_file(path, limit)
        df = pd.DataFrame(lines, columns=["text"])
    else:
        raise ValueError(
            f"Unsupported file type for preview: {ext}. Only CSV, Excel, TXT, and DOCX are supported."
        )

    preview_data = df.head(limit).fillna("").to_dict(orient="records")
    columns = df.columns.tolist()
    return DataPreview(columns=columns, rows=preview_data)


def generate_insights(file_id: str, count: int = 3) -> List[Insight]:
    """
    Simulate insights based on random sampling from the uploaded file.
    Returns a list of Insight schema objects.
    """
    file_path = resolve_file_path(file_id)

    if not file_path:
        raise FileNotFoundException(file_id)

    ext = os.path.splitext(file_path)[1].lower()

    logger.info("[LOG] Attempting to parse file")
    if ext in {".csv", ".xlsx", ".xls"}:
        df = _read_dataframe(file_path, count)
        logger.info("[LOG] Parsed an Excel or CSV file successfully.")
    elif ext in {".txt", "docx"}:
        # read the file to file buffer in-memory, and for the specified count
        # parse the count as "line count",
        # and process the insights on information on `count` lines (count - n) as insights else:
        lines = read_word_text_file(file_path, count)
        df = pd.DataFrame(lines, columns=["text"])
        logger.info("[LOG] Converted Word Document to DataFrame")
    else:
        # we don't recognize the file type and does not provide support for image type
        raise ValueError(
            f"Unsupported file type: {ext}. Only CSV and Excel files are supported."
        )

    # when the processing is done, we will call the OpenRouter.ai API to generate insights
    logger.info("[LOG] Attempting to generate AI insights")
    ai_response = generate_ai_insights(df)  # make a call to OpenAI via OpenRouter.ai
    logger.info("[LOG] Information generated successfully")

    # finally convert the AI response into an Insight Schema object
    # which would later be saved to the filesystem as a JSON file
    # this would be a text content, so we have to cconvert to Insight schema object

    # the approach: 
    # we would jK;; map the list of dicts to Insight models directly
    insights = []
    for i, item in enumerate(ai_response[:count]):
        try:
            insight = Insight(
                title=item.get("title", f"Insight {i + 1}"),
                description=item.get("description", ""),
                confidence_score=item.get("confidence_score", 0.9),
                reference_rows=item.get("reference_rows", []),
            )
            insights.append(insight)
        except Exception as e:
            logger.error(f"[ERROR] Failed to parse insight {i}: {e}")
            continue

    return insights


def read_word_text_file(file_path: str, count: int = 5) -> List[str]:
    """
    Attempts to read a text file, either plain text or Word document,
    and returns the first `count` lines as a block of  text.
    """
    import os

    import docx

    ext = file_path.endswith((".txt", ".docx"))

    if ext == ".docx":
        # use python-docx to read Word documents
        doc = docx.Document(file_path)

        # then read the  first `count` paragraphs
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]

        # just some additional guard: we can never be too sure, return the first `count` paragraphs or all if less than `count`
        return paragraphs[:count] if len(paragraphs) >= count else paragraphs

    else:
        with open(file_path, "r") as f:
            lines = f.readlines()
            return lines[:count] if len(lines) >= count else lines


def persist_insights(file_id: str, insights: List[Insight]) -> None:
    """
    Save generated insights to the filesystem in JSON format.
    """
    path = get_insights_path(file_id)
    try:
        with open(path, "w") as f:
            json.dump([insight.dict() for insight in insights], f)
            logger.info(f"[LOG] Insights saved for file ID: {file_id}")
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
    except FileNotFoundError as e:
        raise InsightsNotFoundException(file_id) from e
    except Exception as e:
        logger.error(f"[RetrieveError] Could not load insights: {e}")
        raise


def _read_dataframe(path: str, count: int = 20) -> pd.DataFrame:
    # Reads a CSV or Excel file based on some row count
    try:
        if path.endswith(".xlsx") or path.endswith(".xls"):
            return pd.read_excel(path, nrows=count)
        return pd.read_csv(path, nrows=count)
    except Exception as e:
        logger.error(f"[ReadError] Could not read file {path}: {e}")
        raise
