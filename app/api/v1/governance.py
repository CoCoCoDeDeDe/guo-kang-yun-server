# app\api\v1\governance.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.governance import GovernanceRecordCreate, GovernanceRecordUpdate, GovernanceRecordResponse
from app.services import governance as governance_service
from app.api.deps import get_current_user, RoleChecker
from app.models.user import User, RoleEnum

router = APIRouter()

# 预定义专家/管理员权限
allow_expert_admin = RoleChecker([RoleEnum.EXPERT, RoleEnum.ADMIN])


@router.post("/", response_model=GovernanceRecordResponse, summary="提交治理记录")
async def create_governance_record(
  record_in: GovernanceRecordCreate,
  db: AsyncSession = Depends(get_db),
  # 👇 任何登录用户都可以发，通过依赖注入获取当前用户对象
  current_user: User = Depends(get_current_user) 
):
  """果农提交自己果园的病虫害治理记录及照片"""
  return await governance_service.create_record(db, record_in=record_in, user_id=current_user.id)


@router.get("/me", response_model=List[GovernanceRecordResponse], summary="获取我的治理记录")
async def read_my_records(
  skip: int = 0, limit: int = 100,
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  """果农查看自己以往提交的治理记录"""
  return await governance_service.get_records_by_user(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/all", response_model=List[GovernanceRecordResponse], summary="获取所有果农的治理记录")
async def read_all_records(
  skip: int = 0, limit: int = 100,
  db: AsyncSession = Depends(get_db),
  # 👇 权限拦截：只有专家或管理员可以纵览所有数据，用于大数据分析或指导
  current_user: User = Depends(allow_expert_admin)
):
  """【仅限专家/管理员】查看所有用户的治理数据"""
  return await governance_service.get_all_records(db, skip=skip, limit=limit)


@router.put("/{record_id}", response_model=GovernanceRecordResponse, summary="更新治理状态")
async def update_governance_record(
  record_id: int,
  record_in: GovernanceRecordUpdate,
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  """修改自己记录的信息，例如将状态从“进行中”修改为“已解决”"""
  record = await governance_service.get_record_by_id(db, record_id)
  if not record:
    raise HTTPException(status_code=404, detail="记录不存在")
    
  # 安全校验：只能修改自己的记录（除非是管理员）
  if record.user_id != current_user.id and current_user.role != RoleEnum.ADMIN:
    raise HTTPException(status_code=403, detail="您无权修改他人的治理记录")
    
  return await governance_service.update_record(db, db_record=record, record_in=record_in)


@router.delete("/{record_id}", summary="删除治理记录")
async def delete_governance_record(
  record_id: int,
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  """删除自己的某条治理记录"""
  record = await governance_service.get_record_by_id(db, record_id)
  if not record:
    raise HTTPException(status_code=404, detail="记录不存在")
    
  # 安全校验：只能删除自己的（或者管理员可删）
  if record.user_id != current_user.id and current_user.role != RoleEnum.ADMIN:
    raise HTTPException(status_code=403, detail="您无权删除他人的治理记录")
    
  await governance_service.delete_record(db, db_record=record)
  return {"msg": "记录删除成功"}