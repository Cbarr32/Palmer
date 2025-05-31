from functools import wraps
import hashlib
import json
import time
from typing import Dict, Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)

class SimpleCache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self, ttl: int = 3600, max_size: int = 1000):
        self.cache: Dict[str, tuple[Any, float]] = {}
        self.ttl = ttl
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def _make_key(self, *args, **kwargs) -> str:
        """Create a cache key from arguments"""
        key_data = {"args": args, "kwargs": kwargs}
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                self.hits += 1
                logger.debug(f"Cache hit for key: {key}")
                return value
            else:
                # Expired
                del self.cache[key]
        
        self.misses += 1
        logger.debug(f"Cache miss for key: {key}")
        return None
    
    def set(self, key: str, value: Any):
        """Set value in cache"""
        # Implement simple LRU by removing oldest entries if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        self.cache[key] = (value, time.time())
        logger.debug(f"Cached value for key: {key}")
    
    def clear(self):
        """Clear all cache entries"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info("Cache cleared")
    
    def stats(self) -> dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.2f}%",
            "size": len(self.cache),
            "max_size": self.max_size
        }

# Global cache instances for different purposes
analysis_cache = SimpleCache(ttl=3600, max_size=500)  # 1 hour TTL
competitor_cache = SimpleCache(ttl=7200, max_size=1000)  # 2 hour TTL

def cached(cache_instance: SimpleCache = None, ttl: int = None):
    """Decorator for caching async function results"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Use provided cache or default
            cache = cache_instance or analysis_cache
            
            # Override TTL if provided
            original_ttl = cache.ttl
            if ttl is not None:
                cache.ttl = ttl
            
            # Skip cache for certain kwargs
            use_cache = kwargs.get("use_cache", True)
            if not use_cache:
                return await func(*args, **kwargs)
            
            # Create cache key
            cache_key = cache._make_key(func.__name__, *args, **kwargs)
            
            # Check cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Call function and cache result
            try:
                result = await func(*args, **kwargs)
                cache.set(cache_key, result)
                return result
            finally:
                # Restore original TTL
                cache.ttl = original_ttl
        
        # Add cache control methods
        wrapper.clear_cache = lambda: cache.clear()
        wrapper.cache_stats = lambda: cache.stats()
        
        return wrapper
    return decorator
