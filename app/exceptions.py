from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import httpx


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Database error",
            "message": "A database error occurred. Please try again later."
        },
    )


async def httpx_exception_handler(request: Request, exc: httpx.RequestError):
    return JSONResponse(
        status_code=503,
        content={
            "error": "External API error",
            "message": "GitHub service is unavailable. Please try again later."
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Something went wrong. Please contact support."
        },
    )
