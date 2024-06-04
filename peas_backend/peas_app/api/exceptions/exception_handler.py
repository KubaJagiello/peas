from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from peas_app.api.logging.logger import logger


class UnableToSaveException(Exception):
    def __init__(self, message: str = "Unable to save the entity"):
        super().__init__(message)


class NotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DatabaseException(Exception):
    def __init__(self, message: str = "", details: Optional[dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


async def database_exception_handler(
    request: Request, exc: DatabaseException
) -> JSONResponse:
    logger.error(
        "DatabaseException occurred",
        exc_info=exc.__cause__,
        extra={
            "message": exc.message,
            "details": exc.details,
            "path": request.url.path,
            "method": request.method,
        },
    )
    raise HTTPException(status_code=500, detail=exc.message) from exc


async def not_found_exception_handler(
    request: Request, exc: NotFoundException
) -> JSONResponse:
    raise HTTPException(status_code=404, detail=exc.message) from exc


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(DatabaseException, database_exception_handler)
