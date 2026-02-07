# app/redis_client.py
import redis.asyncio as redis
from ..configs.configs import get_settings

settings = get_settings()

class RedisClient:
    def __init__(self):
        self.redis_pool = None

    async def connect(self):
        """Initialize the Redis connection pool."""
        self.redis_pool = redis.from_url(
            settings.REDIS_URL, 
            encoding="utf-8", 
            decode_responses=True # Returns strings instead of bytes
        )
        print("Connected to Redis")

    async def close(self):
        """Close the Redis connection."""
        if self.redis_pool:
            await self.redis_pool.close()
            print("Closed Redis connection")
    
    async def get_client(self):
        """Returns the client to be used in routes."""
        if not self.redis_pool:
            await self.connect()
        return self.redis_pool


# Create a singleton instance
redis_app = RedisClient()

# Dependency for Routes
async def get_redis():
    client = await redis_app.get_client()
    try:
        yield client
    finally:
       
        pass