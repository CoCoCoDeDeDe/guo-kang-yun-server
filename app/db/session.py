# app\db\session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# 创建异步引擎
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 创建异步 Session 工厂
AsyncSessionLocal = async_sessionmaker(
  bind=engine,
  class_=AsyncSession,
  expire_on_commit=False,
)

# 依赖注入：用于 FastAPI 路由
async def get_db():
  async with AsyncSessionLocal() as session:
    yield session