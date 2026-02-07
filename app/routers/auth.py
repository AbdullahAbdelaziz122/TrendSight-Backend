from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta

from ..db import database

from ..configs import token
from .. import models
from ..configs.hashing import Hash
router = APIRouter(tags=["Authentication"])

hash = Hash()
@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.User).where(models.User.email == request.username))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    # check password
    if not hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    # generate JWT
    access_token = token.create_access_token(
        data= {'sub': user.email, 'role': user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}