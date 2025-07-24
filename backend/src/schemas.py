from typing import Any, Dict, List

from pydantic import BaseModel, Field


class UploadRequest(BaseModel):
    file: bytes = Field(
        description="Binary content of the file to be uploaded",
    )
    file_name: str = Field(..., description="Name of the file being uploaded")
    file_type: str = Field(..., description="MIME type of the file being uploaded")


class DataPreview(BaseModel):
    columns: List[str]
    rows: List[Dict]


class UploadResponse(BaseModel):
    preview: DataPreview
    file_id: str = Field(description="Unique identifier for the uploaded file")


class ProcessRequest(BaseModel):
    file_id: str = Field(description="Unique identifier for the file to be processed")


class Insight(BaseModel):
    title: str = Field(description="Title of the insight")
    description: str = Field(description="Detailed description of the insight")
    confidence_score: float = Field(
        description="Confidence score of the insight (0 to 1)"
    )
    reference_rows: list[int] = Field(
        description="Row numbers in the file that this insight refers to"
    )


class InsightResponse(BaseModel):
    file_id: str
    insights: list[Insight] = Field(
        description="List of insights extracted from the processed file"
    )
