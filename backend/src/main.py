import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from exceptions import (
    FileNotFoundException,
    FileProcessingError,
    InsightsNotFoundException,
    InvalidFileTypeException,
)
from routes import router as api_router

# env path is located in this directory
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

print("OPENROUTER_API_KEY:", os.getenv("OPENROUTER_API_KEY"))


app = FastAPI(title="AI-powered Insights Cloud", version="1.0.0")
logging.basicConfig(level=logging.INFO)

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Welcome to the File (AI-powered) Insights API. The best you will ever find"
    }


# Our Helper Error Hndlers


@app.exception_handler(FileNotFoundException)
async def file_not_found_exception_handler(
    request: Request, exc: FileNotFoundException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(InsightsNotFoundException)
async def insights_not_found_exception_handler(
    request: Request, exc: InsightsNotFoundException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(InvalidFileTypeException)
async def invalid_file_type_exception_handler(
    request: Request, exc: InvalidFileTypeException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(FileProcessingError)
async def file_processing_error_handler(request: Request, exc: FileProcessingError):
    return JSONResponse(
        status_code=500,
        content={
            "error": exc.code,
            "message": exc.message,
            "details": exc.details,
        },
    )
