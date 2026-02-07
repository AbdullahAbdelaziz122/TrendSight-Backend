from fastapi import FastAPI, Depends, status
from contextlib import asynccontextmanager
import redis.asyncio as redis
from . import models
from .routers import user, auth
from .db.database import engine, check_database_connection
from .db.redis_client import redis_app, get_redis 



async def startup_event():
    print("Starting up...")
    # Initialize DB Tables
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    
    # Connect to Redis
    await redis_app.connect() 

async def shutdown_event():
    print("Shutting down...")
    await redis_app.close() 



@asynccontextmanager
async def lifespan(app: FastAPI):
    
    await startup_event() 
    yield 
    await shutdown_event() 




app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(auth.router)



@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check(
    db_status: bool = Depends(check_database_connection),
    redis_client: redis.Redis = Depends(get_redis)
):
    try:
        await redis_client.ping()
        redis_status = "connected"
    except Exception:
        redis_status = "disconnected"

    return {
        "status": "healthy", 
        "database": "connected", 
        "redis": redis_status
    }