"""
This module defines the API routes for the Insights application.

Approach:

- We need the major endpoints: Upload, Process, and Insights
- Each endpoint will handle specific tasks related to file uploads, processing, and insights retrieval.
- Insights endpoint, will return insights based on the processed data (file in this context).
"""

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from fastapi.background import BackgroundTasks
from fastapi.concurrency import run_in_threadpool
from fastapi.logger import logger
from fastapi.responses import JSONResponse

from schemas import InsightResponse, ProcessRequest, ProcessResponse, UploadResponse
from services import (
    extract_data_preview,
    generate_insights,
    persist_insights,
    process_upload,
    retrieve_saved_insights,
)

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile, request: Request):
    """
    Upload a file to the server.

    This endpoint accepts a file upload and uploads it to our server.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    logger.info(f"Received file: {file.filename}")

    try:
        from fastapi.concurrency import run_in_threadpool

        response = await run_in_threadpool(process_upload, file)
        return response
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail="File upload failed")


@router.post(
    "/process",
    status_code=status.HTTP_201_CREATED,
    response_model=ProcessResponse,
)
def process_file(payload: ProcessRequest):
    """
    Runs a simulation of AI insights generation based on the file ID.

    Accept a file ID and simulate generating AI insights (return 3 insights).
    """

    # approach:
    # - check if the file ID exists
    # - if it exists, generate insights for the uploaded file (return 3 insights)
    # -- each insight should have a title, description, confidence score, and reference rows
    # - if it does not exist, return an error response

    file_id = payload.file_id

    if not file_id:
        raise HTTPException(status_code=400, detail="File ID is required")

    try:
        insights = generate_insights(file_id)

        if not insights:
            raise HTTPException(status_code=404, detail="No insights generated")

        background_t = BackgroundTasks()
        background_t.add_task(persist_insights, file_id, insights)
        # persist_insights(file_id, insights)
        logger.info(f"Insights saved for file ID: {file_id}")

        # return JSONResponse(
        #     status_code=status.HTTP_201_CREATED,
        #     content={
        #         "message": "Insights generated successfully",
        #         "file_id": file_id,
        #         "insights": [insight.dict() for insight in insights],
        #     },
        # )
        return ProcessResponse(
            message="Insights generated successfully",
            file_id=file_id,
            insights=insights,
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found for processing")
    except Exception as e:
        logger.error(f"Processing error for file {file_id}: {e}")
        raise HTTPException(status_code=500, detail="Insight processing failed")


@router.get("/insights", status_code=status.HTTP_200_OK, response_model=InsightResponse)
async def get_insights(file_id: str):
    """
    Retrieve AI-powered insights for the provided file ID if available.

    This endpoint will generate insights based on the uploaded file.

    - We want to allow sorting and filtering here
    """
    if not file_id:
        raise HTTPException(status_code=400, detail="File ID is required")

    try:
        insights = retrieve_saved_insights(file_id)
        return InsightResponse(file_id=file_id, insights=insights)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Insights not found for file ID")
    except Exception as e:
        logger.error(f"Failed to load insights for {file_id}: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve insights")
