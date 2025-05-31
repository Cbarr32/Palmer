"""URL validation utilities"""

import re
from urllib.parse import urlparse, urlunparse
from backend.core.exceptions import InvalidURLError

def validate_url(url: str) -> str:
    """Validate and normalize URL"""
    if not url:
        raise InvalidURLError("", "URL cannot be empty")
    
    # Add https:// if no scheme
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        parsed = urlparse(url)
        
        # Check for valid scheme
        if parsed.scheme not in ['http', 'https']:
            raise InvalidURLError(url, "URL must use http or https scheme")
        
        # Check for netloc
        if not parsed.netloc:
            raise InvalidURLError(url, "URL must include domain")
        
        # Rebuild URL
        return urlunparse(parsed)
        
    except Exception as e:
        raise InvalidURLError(url, str(e))

def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    parsed = urlparse(url)
    return parsed.netloc.lower()
