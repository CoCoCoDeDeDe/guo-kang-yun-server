# app\api\v1\community.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.community import ArticleCreate, ArticleResponse, PostCreate, PostResponse, AuditAction
from app.services import community as community_service
from app.api.deps import get_current_user, RoleChecker
from app.models.user import User, RoleEnum

router = APIRouter()

# 预定义权限
allow_expert_admin = RoleChecker([RoleEnum.EXPERT, RoleEnum.ADMIN])
allow_admin_only = RoleChecker([RoleEnum.ADMIN])


# ==========================
# 科普文章路由
# ==========================
@router.post("/articles", response_model=ArticleResponse, summary="发布科普文章")
async def create_article(
  article_in: ArticleCreate,
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(allow_expert_admin) # 仅限专家和管理员
):
  return await community_service.create_article(db, article_in, current_user.id)

@router.get("/articles", response_model=List[ArticleResponse], summary="浏览科普文章")
async def read_articles(
  skip: int = 0, limit: int = 100,
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  """任何登录用户都可以浏览已经【通过审核(PUBLISHED)】的文章"""
  return await community_service.get_published_articles(db, skip=skip, limit=limit)


# ==========================
# 互动帖子路由
# ==========================
@router.post("/posts", response_model=PostResponse, summary="发布互动帖子")
async def create_post(
  post_in: PostCreate,
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user) # 所有登录用户均可发帖
):
  return await community_service.create_post(db, post_in, current_user.id)

@router.get("/posts", response_model=List[PostResponse], summary="浏览互动帖子")
async def read_posts(
  skip: int = 0, limit: int = 100,
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  """任何登录用户都可以浏览已经【通过审核(PUBLISHED)】的帖子"""
  return await community_service.get_published_posts(db, skip=skip, limit=limit)


# ==========================
# 管理员审核路由
# ==========================
@router.get("/audit/pending", summary="获取待审核内容")
async def get_pending_list(
  target_type: str, # "article" 或 "post"
  skip: int = 0, limit: int = 100,
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(allow_admin_only) # 仅限管理员
):
  if target_type not in ["article", "post"]:
    raise HTTPException(status_code=400, detail="target_type 必须是 'article' 或 'post'")
    
  items = await community_service.get_pending_content(db, target_type, skip, limit)
  return items

@router.post("/audit", summary="执行内容审核")
async def execute_audit_action(
  action: AuditAction,
  db: AsyncSession = Depends(get_db),
  current_user: User = Depends(allow_admin_only) # 仅限管理员
):
  if action.target_type not in ["article", "post"]:
    raise HTTPException(status_code=400, detail="target_type 必须是 'article' 或 'post'")
    
  obj = await community_service.execute_audit(
    db, target_id=action.target_id, target_type=action.target_type,
    auditor_id=current_user.id, is_approved=action.is_approved, feedback=action.feedback
  )
  
  if not obj:
    raise HTTPException(status_code=404, detail="目标内容不存在")
    
  return {"msg": f"审核完成，操作：{'通过' if action.is_approved else '拒绝'}"}