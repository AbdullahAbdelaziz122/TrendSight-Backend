from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import json
import redis.asyncio as redis

from .. import schemas
from ..configs import oauth2
from ..db.database import get_db
from ..repository import userRepository
from ..db.redis_client import get_redis

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#  PUBLIC ROUTE 
@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create(request: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await userRepository.create(request, db)

# ADMIN ONLY ROUTE
@router.get("/", response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
async def get_all(
    db: AsyncSession = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_admin_user)
):
    return await userRepository.get_all(db)

# AUTHENTICATED ROUTE (Any Role) 
@router.get("/{id}", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
async def get_user(
    id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user),
    redis_client: redis.Redis = Depends(get_redis)
):

    # Define unique cache Key
    cache_key = f"user:{id}"

    # check cache
    cached_user = await redis_client.get(cache_key)
    if cached_user:
        print("Cache Hit!")
        return json.loads(cached_user)
    
    print("Cache Miss - Fetching from DB")
    user = await userRepository.get_user(id, db)

    # Save 
    if user:
        user_data = schemas.UserResponse.model_validate(user).model_dump_json()
        await redis_client.set(cache_key, user_data, ex=60)
    
    return user