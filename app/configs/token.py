from .configs import get_settings
from datetime import datetime, timedelta
from jose import jwt, JWTError
from .. import schemas

def create_access_token(data: dict):
    to_encode = data.copy
    expire = datetime.now() + timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode, get_settings().SECRET_KEY, get_settings().ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        
        if email is None:
            raise credentials_exception
        
        return schemas.TokenData(email=email, role=role)
    except JWTError:
        raise credentials_exception