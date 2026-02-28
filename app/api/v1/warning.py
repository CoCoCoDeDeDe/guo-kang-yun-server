# app\api\v1\warning.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.warning import WarningMessageCreate, WarningMessageResponse
from app.services import warning as warning_service
from app.services import user as user_service # <-- 引入用户服务
from app.api.deps import get_current_user, RoleChecker
from app.models.user import User, RoleEnum

from app.services.email import send_warning_email # <-- 引入真实发送邮件的方法

router = APIRouter()

# 预定义权限：只有专家和管理员能发预警
allow_expert_admin = RoleChecker([RoleEnum.EXPERT, RoleEnum.ADMIN])


def send_warning_email_task(warning_title: str, content: str):
  """
  模拟发送预警邮件的后台任务。
  未来你可以在这里引入 fastapi-mail 或 aiosmtplib 去真实请求 SMTP 服务器。
  """
  print("=" * 50)
  print(f"🚀 [后台任务] 正在向所有果农发送邮件广播...")
  print(f"📢 预警标题: 【{warning_title}】")
  print(f"📝 防治建议: {content}")
  print("=" * 50)


@router.post("/", response_model=WarningMessageResponse, summary="发布病虫害预警")
async def publish_warning(
  warning_in: WarningMessageCreate,
  background_tasks: BackgroundTasks, # 注入后台任务对象
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(allow_expert_admin)
):
  """
  【限专家/管理员】发布一条新的病虫害预警。
  发布成功后，系统会在后台自动向用户发送广播邮件。
  """
  # 1. 存入预警数据库
  new_warning = await warning_service.create_warning(db, warning_in)

  # 2. 从数据库提取全体用户的邮箱列表
  user_emails = await user_service.get_all_user_emails(db)

  # 3. 将真实发邮件任务挂载到后台执行
  if user_emails:
    background_tasks.add_task(
      send_warning_email, 
      emails=user_emails, 
      warning_title=new_warning.affected_scope, 
      content=new_warning.prevention_measures
    )
  
  return new_warning


@router.get("/active", response_model=List[WarningMessageResponse], summary="获取当前生效预警")
async def read_active_warnings(
  skip: int = 0, limit: int = 100,
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  """所有登录用户均可查看当前仍在有效期内的预警信息"""
  return await warning_service.get_active_warnings(db, skip=skip, limit=limit)


@router.delete("/{warning_id}", summary="删除预警信息")
async def delete_warning(
  warning_id: int,
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(allow_expert_admin)
):
  """【限专家/管理员】删除某条预警"""
  warning = await warning_service.get_warning_by_id(db, warning_id)
  if not warning:
    raise HTTPException(status_code=404, detail="预警信息不存在")
    
  await warning_service.delete_warning(db, warning)
  return {"msg": "预警信息已撤销"}