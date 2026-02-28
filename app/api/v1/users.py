# app\api\v1\users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user as user_service

router = APIRouter()

@router.post("/register", response_model=UserResponse, summary="用户注册")
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    注册一个新用户
    """
    # 1. 检查邮箱是否已被注册
    existing_user = await user_service.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )
    
    # 2. 创建用户
    new_user = await user_service.create_user(db, user_in=user_in)
    return new_user