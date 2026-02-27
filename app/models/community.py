# app\models\community.py
import enum
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class ContentStatusEnum(str, enum.Enum):
    PENDING = "待审核"
    PUBLISHED = "已发布"

class Article(Base):
  __tablename__ = "articles"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  title: Mapped[str] = mapped_column(String(255), nullable=False)
  content: Mapped[str] = mapped_column(Text, nullable=False)
  category: Mapped[str] = mapped_column(String(50))
  author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  status: Mapped[ContentStatusEnum] = mapped_column(Enum(ContentStatusEnum), default=ContentStatusEnum.PENDING)
  views: Mapped[int] = mapped_column(Integer, default=0)
  create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

  author: Mapped["User"] = relationship(back_populates="articles")

class Post(Base):
  __tablename__ = "posts"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  title: Mapped[str] = mapped_column(String(255), nullable=False)
  content: Mapped[str] = mapped_column(Text, nullable=False)
  category: Mapped[str] = mapped_column(String(50))
  author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  status: Mapped[ContentStatusEnum] = mapped_column(Enum(ContentStatusEnum), default=ContentStatusEnum.PENDING)
  views: Mapped[int] = mapped_column(Integer, default=0)
  create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

  author: Mapped["User"] = relationship(back_populates="posts")

class AuditLog(Base):
  __tablename__ = "audit_logs"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  target_id: Mapped[int] = mapped_column(Integer, nullable=False)
  target_type: Mapped[str] = mapped_column(String(50))
  auditor_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
  result: Mapped[str] = mapped_column(String(50))
  feedback: Mapped[Optional[str]] = mapped_column(Text)
  audit_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))