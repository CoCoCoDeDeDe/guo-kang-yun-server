# app\db\database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# ======================================
# 声明式基类（供 app/models/ 下的模型继承）
# ======================================
class Base(DeclarativeBase):
  """
  SQLAlchemy 2.0 声明基类
  所有模型表都应该继承此类
  """
  pass

# ======================================
# 数据库连接与 Session 管理
# ======================================
# 创建异步引擎
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 创建异步 Session 工厂
AsyncSessionLocal = async_sessionmaker(
  bind=engine,
  class_=AsyncSession,
  expire_on_commit=False,
)

# ======================================
# 依赖注入 （供 FastAPI 路由使用）
# ======================================
async def get_db():
  """
  获取数据库
  """
  async with AsyncSessionLocal() as session:
    yield session