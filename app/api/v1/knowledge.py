# app\api\v1\knowledge.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.knowledge import PestInfoCreate, PestInfoUpdate, PestInfoResponse
from app.services import knowledge as knowledge_service
from app.api.deps import get_current_user, RoleChecker
from app.models.user import User, RoleEnum

router = APIRouter()

# 预定义权限依赖
allow_expert_admin = RoleChecker([RoleEnum.EXPERT, RoleEnum.ADMIN])
allow_admin_only = RoleChecker([RoleEnum.ADMIN])


@router.post("/pests", response_model=PestInfoResponse, summary="发布病虫害信息")
async def create_pest_info(
  pest_in: PestInfoCreate,
  db: AsyncSession = Depends(get_db),
  # 👇 权限拦截：仅专家和管理员可访问
  current_user: User = Depends(allow_expert_admin)
):
  return await knowledge_service.create_pest(db, pest_in)


@router.get("/pests", response_model=List[PestInfoResponse], summary="获取病虫害列表")
async def read_pests(
  skip: int = 0, 
  limit: int = 100,
  db: AsyncSession = Depends(get_db),
  # 👇 仅需登录即可访问 (果农可以看)
  current_user: User = Depends(get_current_user)
):
  return await knowledge_service.get_pest_list(db, skip=skip, limit=limit)


@router.get("/pests/{pest_id}", response_model=PestInfoResponse, summary="获取病虫害详情")
async def read_pest(
  pest_id: int,
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  pest = await knowledge_service.get_pest_by_id(db, pest_id)
  if not pest:
    raise HTTPException(status_code=404, detail="未找到该病虫害信息")
  return pest


@router.put("/pests/{pest_id}", response_model=PestInfoResponse, summary="更新病虫害信息")
async def update_pest_info(
  pest_id: int,
  pest_in: PestInfoUpdate,
  db: AsyncSession = Depends(get_db),
  # 👇 权限拦截：仅专家和管理员可访问
  current_user: User = Depends(allow_expert_admin)
):
  pest = await knowledge_service.get_pest_by_id(db, pest_id)
  if not pest:
    raise HTTPException(status_code=404, detail="未找到该病虫害信息")
  return await knowledge_service.update_pest(db, db_pest=pest, pest_in=pest_in)


@router.delete("/pests/{pest_id}", summary="删除病虫害信息")
async def delete_pest_info(
  pest_id: int,
  db: AsyncSession = Depends(get_db),
  # 👇 权限拦截：为了数据安全，删除操作仅限【管理员】
  current_user: User = Depends(allow_admin_only)
):
  pest = await knowledge_service.get_pest_by_id(db, pest_id)
  if not pest:
    raise HTTPException(status_code=404, detail="未找到该病虫害信息")
  
  await knowledge_service.delete_pest(db, db_pest=pest)
  return {"msg": "病虫害信息已成功删除"}