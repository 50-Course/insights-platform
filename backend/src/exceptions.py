class Exception(Exception):
    """Base class for all exceptions in this module."""

    pass


class FileProcessingError(Exception):
    """Exception raised for errors in file processing."""

    def __init__(self, message, code=None, details=None):
        super().__init__(message)
        self.code = code or "FILE_PROCESSING_ERROR"
        self.message = message
        self.details = details or {}
