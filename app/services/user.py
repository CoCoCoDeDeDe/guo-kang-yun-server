# app\services\user.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import bcrypt  # <-- 改为导入 bcrypt

from app.models.user import User
from app.schemas.user import UserCreate

# ====== 替换原来的 pwd_context 和 相关函数 ======

def get_password_hash(password: str) -> str:
    """将明文密码转化为哈希值"""
    # bcrypt 需要 bytes 格式的字符串，所以要 encode
    pwd_bytes = password.encode('utf-8')
    # 生成盐并哈希
    hashed_bytes = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    # 存入数据库的是字符串格式，所以再 decode 回来
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否正确"""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# ================================================

# 下面的查询和创建逻辑完全保持不变
async def get_user_by_email(db: AsyncSession, email: str):
    """根据邮箱查询用户"""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_in: UserCreate):
    """创建新用户"""
    hashed_password = get_password_hash(user_in.password)
    
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        password=hashed_password,
        role=user_in.role,
        phone=user_in.phone
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user) 
    
    return db_user
  
async def authenticate_user(db: AsyncSession, email: str, password: str):
  """
  验证用户登录：比对邮箱和密码
  """
  user = await get_user_by_email(db, email)
  if not user:
    return False
  
  if not verify_password(password, user.password):
    return False
      
  return user

async def get_all_user_emails(db: AsyncSession) -> list[str]:
  """获取系统中所有用户的邮箱列表"""
  # 如果你只想发给果农，可以加 .where(User.role == RoleEnum.FARMER)
  result = await db.execute(select(User.email))
  return result.scalars().all()

async def update_user_password(db: AsyncSession, user: User, new_password: str):
  """
  修改用户密码：生成新哈希值并保存到数据库
  """
  # 将新密码进行哈希加密
  hashed_password = get_password_hash(new_password)
  
  # 更新对象并提交
  user.password = hashed_password
  db.add(user)
  await db.commit()
  await db.refresh(user)
  return user