# app\schemas\community.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.models.community import ContentStatusEnum

# --- Article Schemas ---
class ArticleBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    category: str = Field(..., max_length=50)

class ArticleCreate(ArticleBase):
    author_id: int

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
    author_id: int

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