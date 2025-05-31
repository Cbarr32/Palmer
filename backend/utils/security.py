"""Security utilities"""

import secrets
import hashlib
from typing import List, Optional

class SecurityManager:
    """Security management utilities"""
    
    def __init__(self):
        self.api_keys: List[str] = [
            "test-api-key-123",  # Remove in production
        ]
    
    def verify_api_key(self, api_key: str) -> bool:
        """Verify API key"""
        # In production, check against database
        return api_key in self.api_keys
    
    def generate_api_key(self) -> str:
        """Generate new API key"""
        return f"pk_{secrets.token_urlsafe(32)}"
    
    def hash_api_key(self, api_key: str) -> str:
        """Hash API key for storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()
