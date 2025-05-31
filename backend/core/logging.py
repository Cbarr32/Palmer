"""Logging configuration for Palmer Intelligence API"""

import logging
import sys
from typing import Optional

def setup_logging(name: Optional[str] = None) -> logging.Logger:
    """Setup logging configuration"""
    
    logger = logging.getLogger(name or "palmer_api")
    
    log_level = logging.INFO
    if hasattr(logging, 'DEBUG'):
        from backend.core.config import settings
        log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    logger.setLevel(log_level)
    
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()
