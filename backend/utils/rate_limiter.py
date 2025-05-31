"""Rate limiting utilities"""

import time
from typing import Optional
import redis.asyncio as redis

class RateLimiter:
    """Rate limiter implementation"""
    
    def __init__(self, redis_client: Optional[redis.Redis], requests_per_minute: int = 60, requests_per_hour: int = 1000):
        self.redis_client = redis_client
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
    
    async def check_limit(self, key: str) -> bool:
        """Check if request is within rate limit"""
        if not self.redis_client:
            return True
        
        try:
            current_time = int(time.time())
            minute_key = f"rate_limit:{key}:minute:{current_time // 60}"
            hour_key = f"rate_limit:{key}:hour:{current_time // 3600}"
            
            # Check minute limit
            minute_count = await self.redis_client.incr(minute_key)
            if minute_count == 1:
                await self.redis_client.expire(minute_key, 60)
            
            if minute_count > self.requests_per_minute:
                return False
            
            # Check hour limit
            hour_count = await self.redis_client.incr(hour_key)
            if hour_count == 1:
                await self.redis_client.expire(hour_key, 3600)
            
            if hour_count > self.requests_per_hour:
                return False
            
            return True
            
        except Exception:
            # If Redis fails, allow request
            return True
