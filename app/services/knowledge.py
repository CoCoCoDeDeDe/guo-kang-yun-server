# app\services\knowledge.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.knowledge import PestInfo
from app.schemas.knowledge import PestInfoCreate, PestInfoUpdate

async def get_pest_list(db: AsyncSession, skip: int = 0, limit: int = 100):
  """获取病虫害列表（包含关联的防治方案）"""
  # 异步查询必须显式使用 selectinload 来加载关联关系 (prevention_schemes)
  stmt = select(PestInfo).options(selectinload(PestInfo.prevention_schemes)).offset(skip).limit(limit)
  result = await db.execute(stmt)
  return result.scalars().all()

async def get_pest_by_id(db: AsyncSession, pest_id: int):
  """根据ID获取单个病虫害详情"""
  stmt = select(PestInfo).options(selectinload(PestInfo.prevention_schemes)).where(PestInfo.id == pest_id)
  result = await db.execute(stmt)
  return result.scalar_one_or_none()

async def create_pest(db: AsyncSession, pest_in: PestInfoCreate):
  """创建病虫害记录"""
  # 使用 Pydantic V2 的 model_dump() 方法将 schema 转为字典
  db_pest = PestInfo(**pest_in.model_dump())
  db.add(db_pest)
  await db.commit()

  # ❌ 删掉原本的 await db.refresh(db_pest)
  # ✅ 改为显式查询，把关联的 prevention_schemes 一起查出来喂给 Pydantic
  stmt = select(PestInfo).options(selectinload(PestInfo.prevention_schemes)).where(PestInfo.id == db_pest.id)
  result = await db.execute(stmt)
  return result.scalar_one()

async def update_pest(db: AsyncSession, db_pest: PestInfo, pest_in: PestInfoUpdate):
  """更新病虫害记录"""
  # exclude_unset=True 确保只更新前端传过来的字段
  update_data = pest_in.model_dump(exclude_unset=True)
  for field, value in update_data.items():
    setattr(db_pest, field, value)
      
  await db.commit()
  
  # ❌ 同理，删掉原本的 await db.refresh(db_pest)
  # ✅ 重新查询加载关系
  stmt = select(PestInfo).options(selectinload(PestInfo.prevention_schemes)).where(PestInfo.id == db_pest.id)
  result = await db.execute(stmt)
  return result.scalar_one()

async def delete_pest(db: AsyncSession, db_pest: PestInfo):
  """删除病虫害记录"""
  await db.delete(db_pest)
  await db.commit()
  return db_pest