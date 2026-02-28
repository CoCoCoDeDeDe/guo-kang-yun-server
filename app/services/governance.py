# app\services\governance.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.governance import GovernanceRecord
from app.schemas.governance import GovernanceRecordCreate, GovernanceRecordUpdate

async def create_record(db: AsyncSession, record_in: GovernanceRecordCreate, user_id: int):
  """创建一条新的治理记录，并绑定到当前用户"""
  # model_dump() 提取前端传来的数据，同时手动塞入从 Token 解析出的 user_id
  db_record = GovernanceRecord(**record_in.model_dump(), user_id=user_id)
  db.add(db_record)
  await db.commit()
  await db.refresh(db_record)
  return db_record

async def get_records_by_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
  """获取指定用户（如当前果农）的所有记录"""
  stmt = select(GovernanceRecord).where(GovernanceRecord.user_id == user_id).offset(skip).limit(limit)
  result = await db.execute(stmt)
  return result.scalars().all()

async def get_all_records(db: AsyncSession, skip: int = 0, limit: int = 100):
  """获取系统中的所有治理记录（供专家/管理员查看）"""
  stmt = select(GovernanceRecord).offset(skip).limit(limit)
  result = await db.execute(stmt)
  return result.scalars().all()

async def get_record_by_id(db: AsyncSession, record_id: int):
  """根据 ID 获取单条记录"""
  stmt = select(GovernanceRecord).where(GovernanceRecord.id == record_id)
  result = await db.execute(stmt)
  return result.scalar_one_or_none()

async def update_record(db: AsyncSession, db_record: GovernanceRecord, record_in: GovernanceRecordUpdate):
  """更新治理记录"""
  update_data = record_in.model_dump(exclude_unset=True)
  for field, value in update_data.items():
    setattr(db_record, field, value)
    
  await db.commit()
  await db.refresh(db_record)
  return db_record

async def delete_record(db: AsyncSession, db_record: GovernanceRecord):
  """删除治理记录"""
  await db.delete(db_record)
  await db.commit()
  return db_record