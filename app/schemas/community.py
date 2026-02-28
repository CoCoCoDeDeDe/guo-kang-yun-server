# app\schemas\community.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.models.community import ContentStatusEnum

from pydantic import BaseModel

# --- Article Schemas ---
class ArticleBase(BaseModel):
  title: str = Field(..., max_length=255)
  content: str
  category: str = Field(..., max_length=50)

class ArticleCreate(ArticleBase):
  # 通过权限验证依赖注入获取 author user 数据
  # author_id: int
  pass

class ArticleUpdate(BaseModel):
  title: Optional[str] = Field(None, max_length=255)
  content: Optional[str] = None
  category: Optional[str] = Field(None, max_length=50)
  status: Optional[ContentStatusEnum] = None

class ArticleResponse(ArticleBase):
  id: int
  author_id: int
  status: ContentStatusEnum
  views: int
  create_at: datetime

  model_config = ConfigDict(from_attributes=True)

# --- Post Schemas ---
class PostBase(BaseModel):
  title: str = Field(..., max_length=255)
  content: str
  category: str = Field(..., max_length=50)

class PostCreate(PostBase):
  # author_id: int
  pass

class PostResponse(PostBase):
  id: int
  author_id: int
  status: ContentStatusEnum
  views: int
  create_at: datetime

  model_config = ConfigDict(from_attributes=True)

# --- AuditLog Schemas ---
class AuditLogBase(BaseModel):
  target_id: int
  target_type: str = Field(..., max_length=50)
  result: str = Field(..., max_length=50)
  feedback: Optional[str] = None

class AuditLogCreate(AuditLogBase):
  auditor_id: int

class AuditLogResponse(AuditLogBase):
  id: int
  auditor_id: Optional[int]
  audit_time: datetime

  model_config = ConfigDict(from_attributes=True)
  
# 新增一个用于接收审核请求的 Schema
class AuditAction(BaseModel):
    target_id: int
    target_type: str  # "article" 或 "post"
    is_approved: bool # True: 通过, False: 拒绝
    feedback: str | None = None