# app\api\v1\users.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # 引入 OAuth2 表单
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token # 引入 Token schem
from app.services import user as user_service
from app.core.security import create_access_token # 引入生成 token 方法

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

@router.post("/login", response_model=Token, summary="用户登录 (获取Token)")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    使用 OAuth2 密码流登录获取 JWT Token。
    注意：OAuth2 规范中账号字段名固定为 `username`，前端在这里请传入**邮箱**。
    """
    # 这里 form_data.username 实际上接收的是用户填写的邮箱
    user = await user_service.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 生成 Token，通常把用户 ID 存入 Token 的 "sub" (主题) 字段中
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # 必须严格按照包含 access_token 和 token_type 的字典返回
    return {"access_token": access_token, "token_type": "bearer"}