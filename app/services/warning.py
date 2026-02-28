# app\services\warning.py
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.warning import WarningMessage
from app.schemas.warning import WarningMessageCreate, WarningMessageUpdate

async def create_warning(db: AsyncSession, warning_in: WarningMessageCreate):
  """创建预警信息"""
  db_obj = WarningMessage(**warning_in.model_dump())
  db.add(db_obj)
  await db.commit()
  await db.refresh(db_obj)
  return db_obj

async def get_active_warnings(db: AsyncSession, skip: int = 0, limit: int = 100):
  """获取仍在【有效期内】的预警信息"""
  now = datetime.now(timezone.utc)
  # 查询条件：过期时间大于当前时间
  stmt = select(WarningMessage).where(WarningMessage.expire_time > now).order_by(WarningMessage.publish_time.desc()).offset(skip).limit(limit)
  result = await db.execute(stmt)
  return result.scalars().all()

async def get_warning_by_id(db: AsyncSession, warning_id: int):
  """根据ID查询预警"""
  stmt = select(WarningMessage).where(WarningMessage.id == warning_id)
  result = await db.execute(stmt)
  return result.scalar_one_or_none()

async def delete_warning(db: AsyncSession, db_warning: WarningMessage):
  """删除预警信息"""
  await db.delete(db_warning)
  await db.commit()
  return db_warning