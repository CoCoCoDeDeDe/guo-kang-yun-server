# app\schemas\user.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# 直接从模型中导入 Enum 避免重复定义
from app.models.user import RoleEnum

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., max_length=100)
    role: RoleEnum = RoleEnum.FARMER
    phone: Optional[str] = Field(None, max_length=20)
    is_verified: int = 0

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="明文密码，后端需哈希处理")

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    password: Optional[str] = Field(None, min_length=6)

class UserResponse(UserBase):
    id: int
    create_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- VerificationCode Schemas ---
class VerificationCodeBase(BaseModel):
    email: EmailStr
    code: str = Field(..., max_length=10)
    type: str = Field(..., max_length=50)

class VerificationCodeCreate(VerificationCodeBase):
    expire_at: datetime

class VerificationCodeResponse(VerificationCodeBase):
    id: int
    expire_at: datetime
    is_used: bool
    create_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Token Schemas ---
class Token(BaseModel):
  access_token: str
  token_type: str