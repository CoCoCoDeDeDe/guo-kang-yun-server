# app/core/security.py
from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """生成 JWT Token"""
    to_encode = data.copy()
    
    # 设置过期时间
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    
    # 使用密钥和算法进行签名
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt