from .configs import get_settings
from datetime import datetime, timedelta, timezone  
from jose import jwt, JWTError
from .. import schemas

settings = get_settings() 

def create_access_token(data: dict):
    to_encode = data.copy() 
    
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({'exp': expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        email: str = payload.get("sub")
        role: str = payload.get("role")
        
        if email is None:
            raise credentials_exception
        
        return schemas.TokenData(email=email, role=role)
    except JWTError:
        raise credentials_exception