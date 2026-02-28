# app\services\community.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from app.models.community import Article, Post, AuditLog, ContentStatusEnum
from app.schemas.community import ArticleCreate, PostCreate

# ==========================================
# 1. 科普文章 (Articles) 服务
# ==========================================
async def create_article(db: AsyncSession, article_in: ArticleCreate, author_id: int):
  """发布科普文章 (默认状态为待审核)"""
  db_obj = Article(**article_in.model_dump(), author_id=author_id)
  db.add(db_obj)
  await db.commit()
  await db.refresh(db_obj)
  return db_obj

async def get_published_articles(db: AsyncSession, skip: int = 0, limit: int = 100):
  """获取已发布的文章列表 (任何人可看)"""
  stmt = select(Article).where(Article.status == ContentStatusEnum.PUBLISHED).offset(skip).limit(limit)
  result = await db.execute(stmt)
  return result.scalars().all()

# ==========================================
# 2. 互动帖子 (Posts) 服务
# ==========================================
async def create_post(db: AsyncSession, post_in: PostCreate, author_id: int):
  """发布互动帖子 (默认状态为待审核)"""
  db_obj = Post(**post_in.model_dump(), author_id=author_id)
  db.add(db_obj)
  await db.commit()
  await db.refresh(db_obj)
  return db_obj

async def get_published_posts(db: AsyncSession, skip: int = 0, limit: int = 100):
  """获取已发布的帖子列表"""
  stmt = select(Post).where(Post.status == ContentStatusEnum.PUBLISHED).offset(skip).limit(limit)
  result = await db.execute(stmt)
  return result.scalars().all()

# ==========================================
# 3. 审核 (Audit) 服务
# ==========================================
async def get_pending_content(db: AsyncSession, target_type: str, skip: int = 0, limit: int = 100):
  """获取待审核的内容"""
  model = Article if target_type == "article" else Post
  stmt = select(model).where(model.status == ContentStatusEnum.PENDING).offset(skip).limit(limit)
  result = await db.execute(stmt)
  return result.scalars().all()

async def execute_audit(db: AsyncSession, target_id: int, target_type: str, auditor_id: int, is_approved: bool, feedback: str):
  """执行审核操作"""
  model = Article if target_type == "article" else Post
  
  # 查询目标内容
  result = await db.execute(select(model).where(model.id == target_id))
  target_obj = result.scalar_one_or_none()
  
  if not target_obj:
    return None

  # 如果通过，则更新状态为已发布；如果拒绝，可以保持待审核或后续加个“已拒绝”状态
  if is_approved:
    target_obj.status = ContentStatusEnum.PUBLISHED

  # 记录审核日志
  log = AuditLog(
    target_id=target_id,
    target_type=target_type,
    auditor_id=auditor_id,
    result="通过" if is_approved else "拒绝",
    feedback=feedback
  )
  db.add(log)
  await db.commit()
  return target_obj