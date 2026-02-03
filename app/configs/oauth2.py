from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import token
from .. import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Base Dependency: Get Current User (Any Role)
def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    return token.verify_token(data, credentials_exception)

# Authorization Dependency: Only Admin
def get_current_admin_user(current_user: schemas.TokenData = Depends(get_current_user)):
    # Check if the role in the token matches 'admin'
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
    return current_user