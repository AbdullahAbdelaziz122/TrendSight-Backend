from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from .. import models, schemas
from ..configs.hashing import Hash

hash = Hash()

async def create(request: schemas.UserCreate, db: AsyncSession):
   
    new_user = models.User(
        email=request.email,
        password=hash.get_password_hash(request.password),
        role=request.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user(id: int, db: AsyncSession):
    
    result = await db.execute(select(models.User).where(models.User.id == id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found"
        )
    return user

async def get_all(db: AsyncSession):
    result = await db.execute(select(models.User))
    
    return result.scalars().all()

async def update_user(id: int, request: schemas.UserCreate, db: AsyncSession):
    
    result = await db.execute(select(models.User).where(models.User.id == id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found"
        )
    
    
    user.email = request.email
    user.role = request.role 
    if request.password:
        user.password = hash.get_password_hash(request.password)
    
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(id: int, db: AsyncSession):
    result = await db.execute(select(models.User).where(models.User.id == id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found"
        )
    
    await db.delete(user)
    await db.commit()
    return {"detail": "User deleted"}