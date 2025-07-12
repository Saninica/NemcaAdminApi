from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from src.schemas.auth import TokenData
import uuid


SECRET_KEY = "your_secret_key"  # Gerçek projelerde çevresel değişkenlerden alınmalı
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Token blacklist - in production, use Redis or database
TOKEN_BLACKLIST = set()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    
    # Add JTI (JWT ID) for token tracking
    jti = str(uuid.uuid4())
    to_encode.update({"exp": expire, "jti": jti})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        jti: str = payload.get("jti")
        
        if username is None or jti is None:
            raise credentials_exception
            
        # Check if token is blacklisted
        if jti in TOKEN_BLACKLIST:
            raise credentials_exception
            
        token_data = TokenData(username=username, jti=jti)
        return token_data
    except JWTError:
        raise credentials_exception

def blacklist_token(jti: str):
    """Add token JTI to blacklist"""
    TOKEN_BLACKLIST.add(jti)

def is_token_blacklisted(jti: str) -> bool:
    """Check if token JTI is blacklisted"""
    return jti in TOKEN_BLACKLIST
