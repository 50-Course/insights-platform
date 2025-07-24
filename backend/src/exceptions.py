from fastapi.exceptions import HTTPException


class FileNotFoundException(HTTPException):
    def __init__(self, file_id: str):
        super().__init__(
            status_code=404, detail=f"File not found for file ID: {file_id}"
        )


class InsightsNotFoundException(HTTPException):
    def __init__(self, file_id: str):
        super().__init__(
            status_code=404, detail=f"Insights not found or No saved insights for file ID: {file_id}"
        )


class InvalidFileTypeException(HTTPException):
    def __init__(self, file_type: str):
        super().__init__(status_code=400, detail=f"Unsupported file type: {file_type}")


class FileProcessingError(Exception):
    """Exception raised for errors in file processing."""

    def __init__(self, message, code=None, details=None):
        super().__init__(message)
        self.code = code or "FILE_PROCESSING_ERROR"
        self.message = message
        self.details = details or {}
