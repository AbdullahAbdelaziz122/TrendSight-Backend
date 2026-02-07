import asyncio
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..configs.configs import get_settings
from sqlalchemy import text
settings = get_settings()

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# create_async_engine 
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True, # Set to False in production
)

# AsyncSession
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()

# Dependency for FastAPI routes
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


async def check_database_connection(db: AsyncSession = Depends(get_db)):
    try:
        # A simple, non-blocking query to check connectivity
        await db.execute(text("SELECT 1"))
        return True
    except Exception as e:
        # Log the error (optional)
        print(f"Database check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )