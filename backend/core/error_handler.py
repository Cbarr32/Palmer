from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import logging
import traceback
from typing import Union

logger = logging.getLogger(__name__)

class APIError(HTTPException):
    def __init__(self, status_code: int, message: str, detail: Union[str, dict] = None):
        super().__init__(
            status_code=status_code, 
            detail={"message": message, "detail": detail, "success": False}
        )

class ValidationError(APIError):
    def __init__(self, message: str, detail: Union[str, dict] = None):
        super().__init__(status_code=400, message=message, detail=detail)

class NotFoundError(APIError):
    def __init__(self, message: str, detail: Union[str, dict] = None):
        super().__init__(status_code=404, message=message, detail=detail)

class RateLimitError(APIError):
    def __init__(self, message: str = "Rate limit exceeded", detail: Union[str, dict] = None):
        super().__init__(status_code=429, message=message, detail=detail)

class ExternalServiceError(APIError):
    def __init__(self, message: str = "External service error", detail: Union[str, dict] = None):
        super().__init__(status_code=502, message=message, detail=detail)

async def api_error_handler(request: Request, exc: Exception):
    """Global error handler for unhandled exceptions"""
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    
    # Get debug mode from app state
    debug = getattr(request.app.state, "debug", False)
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "detail": str(exc) if debug else None,
            "traceback": traceback.format_exc() if debug else None
        }
    )

async def validation_error_handler(request: Request, exc: ValidationError):
    """Handler for validation errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

def wrap_endpoint(func):
    """Decorator to wrap endpoints with error handling"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            raise APIError(
                status_code=500,
                message="Internal server error",
                detail=str(e)
            )
    
    wrapper.__name__ = func.__name__
    return wrapper
