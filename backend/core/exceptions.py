"""Custom exceptions for Palmer Intelligence API"""

from typing import Optional, Dict, Any

class PalmerAPIException(Exception):
    """Base exception for Palmer API"""
    def __init__(self, message: str, code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.code = code or "PALMER_ERROR"
        self.details = details or {}
        super().__init__(self.message)

class AnalysisError(PalmerAPIException):
    """Raised when analysis fails"""
    def __init__(self, message: str, code: str = "ANALYSIS_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code, details)

class RateLimitError(PalmerAPIException):
    """Raised when rate limit is exceeded"""
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__(message, "RATE_LIMIT_EXCEEDED", {"retry_after": retry_after})

class InvalidURLError(PalmerAPIException):
    """Raised when URL is invalid"""
    def __init__(self, url: str, message: Optional[str] = None):
        msg = message or f"Invalid URL: {url}"
        super().__init__(msg, "INVALID_URL", {"url": url})

class InsufficientDataError(PalmerAPIException):
    """Raised when insufficient data for analysis"""
    def __init__(self, message: str = "Insufficient data for analysis"):
        super().__init__(message, "INSUFFICIENT_DATA")

class AuthenticationError(PalmerAPIException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTH_ERROR")
