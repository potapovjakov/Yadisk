from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.responses import JSONResponse


class Error(BaseModel):
    code: int
    message: str


class InvalidRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class NotFoundException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def create_exceptions(app: FastAPI):
    @app.exception_handler(InvalidRequestException)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(Error(code=400, message=str(exc)).dict(),
                            status_code=400)

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request, exc):
        return JSONResponse(Error(code=404, message=str(exc)).dict(),
                            status_code=404)
