# app\api\v1\users.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # 引入 OAuth2 表单
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token # 引入 Token schem
from app.services import user as user_service
from app.core.security import create_access_token # 引入生成 token 方法
from app.api.deps import get_current_user
from app.models.user import User

from app.api.deps import get_current_user, RoleChecker 
from app.models.user import User, RoleEnum

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
  
@router.get("/me", response_model=UserResponse, summary="获取当前登录用户信息")
async def read_users_me(current_user: User = Depends(get_current_user)):
  """
  获取当前登录用户自己的信息。
  这是一个受保护的接口，必须在 Header 中携带有效的 JWT Token 才能访问。
  """
  # 只要能走到这里，说明 Token 验证绝对通过了，并且 current_user 就是数据库里查出来的真实用户对象！
  return current_user

# ==========================================
# 权限受控接口演示
# ==========================================

# 1. 定义具体的权限依赖
# 只要是专家或管理员都可以访问
allow_expert_admin = RoleChecker([RoleEnum.EXPERT, RoleEnum.ADMIN])
# 仅限管理员访问
allow_admin_only = RoleChecker([RoleEnum.ADMIN])

@router.post("/expert/publish-pest", summary="【权限测试】发布病虫害信息")
async def publish_pest_info(
  # 使用 Depends(allow_expert_admin) 替代原来的 Depends(get_current_user)
  current_user: User = Depends(allow_expert_admin) 
):
  """
  模拟一个只有专家或管理员才能调用的接口（例如发布新的病虫害科普）。
  如果是果农（role=0）调用，会直接返回 403 Forbidden。
  """
  return {
    "msg": "验证通过！", 
    "user": current_user.username, 
    "role_name": current_user.role.name,
    "action": "你可以发布病虫害信息"
  }

@router.delete("/admin/delete-user", summary="【权限测试】删除用户")
async def delete_user_demo(
  current_user: User = Depends(allow_admin_only)
):
  """
  模拟一个极其敏感的接口，仅管理员可调用。
  """
  return {
    "msg": "验证通过！", 
    "user": current_user.username, 
    "action": "你是管理员，你有权删除用户"
  }