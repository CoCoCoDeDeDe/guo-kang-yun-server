# app\api\deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.db.database import get_db
from app.models.user import User

from typing import List
from app.models.user import RoleEnum

# 定义 OAuth2 的 Token 来源
# 这个 URL 就是告诉 Swagger UI 上的小锁，去哪里调用接口换取 Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

async def get_current_user(
  token: str = Depends(oauth2_scheme), 
  db: AsyncSession = Depends(get_db)
) -> User:
  """
  解析 Token 并获取当前登录用户
  """
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="认证失败，无效的 Token 或 Token 已过期",
    headers={"WWW-Authenticate": "Bearer"},
  )
  
  try:
    # 1. 使用与生成时相同的秘钥和算法解析 Token
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
    # 2. 提取我们在 login 接口里放进去的 "sub" (主题/用户ID)
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
        
    # 转回整数以便查库
    user_id = int(user_id_str)
      
  except InvalidTokenError:
    # 解析失败（如 Token 被篡改或已过期）直接抛出 401
    raise credentials_exception

  # 3. 去数据库查询此用户
  result = await db.execute(select(User).where(User.id == user_id))
  user = result.scalar_one_or_none()
  
  if user is None:
    raise credentials_exception
      
  return user

class RoleChecker:
  """
  权限校验依赖类
  允许传入一个或多个允许访问的角色列表
  """
  def __init__(self, allowed_roles: List[RoleEnum]):
    self.allowed_roles = allowed_roles

  def __call__(self, current_user: User = Depends(get_current_user)) -> User:
    """
    FastAPI 在解析依赖时会自动调用 __call__。
    这里先通过 get_current_user 获取到当前用户，然后判断其角色。
    """
    if current_user.role not in self.allowed_roles:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="权限不足，无法执行此操作"
      )
    return current_user
