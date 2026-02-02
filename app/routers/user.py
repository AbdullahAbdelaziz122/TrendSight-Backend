from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .. import schemas
from ..database import get_db
from ..repository import userRepository

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create(request: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    
    return await userRepository.create(request, db)


@router.get("/", response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
async def get_all(db: AsyncSession = Depends(get_db)):

    return await userRepository.get_all(db)



@router.get("/{id}", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    
    return await userRepository.get_user(id, db)



@router.put("/{id}", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
async def update_user(id: int, request: schemas.UserCreate, db: AsyncSession = Depends(get_db)):

    return await userRepository.update_user(id, request, db)



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) 
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    await userRepository.delete_user(id, db)
    return None