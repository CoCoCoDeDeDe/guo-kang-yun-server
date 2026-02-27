# app\models\user.py
# Outer
from enum import IntEnum
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Mine
from app.db.database import Base

# class RoleEnum(int, Enum): # A
# class RoleEnum(Enum): # B 不支持 RoleEnum(数字)
class RoleEnum(IntEnum): # C 等效 A
  FARMER = 0
  EXPERT = 1
  ADMIN = 2
  
# print(RoleEnum)
# print(type(RoleEnum))
# print(RoleEnum.ADMIN)
# print(type(RoleEnum.ADMIN))
# print(RoleEnum.ADMIN.name)
# print(RoleEnum.ADMIN.value)
# print(RoleEnum(0))
# print(RoleEnum(3)) # 运行后报错

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
  username: Mapped[str] = mapped_column(String(100), nullable=False)
  password: Mapped[str] = mapped_column(String(255), nullable=False)
  role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.FARMER, nullable=False)
  phone: Mapped[Optional[str]] = mapped_column(String(20))
  is_verified: Mapped[int] = mapped_column(Integer, default=0, comment="0-未激活, 1-已激活")
  create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

  # 使用字符串类名避免循环导入
  governance_records: Mapped[List["GovernanceRecord"]] = relationship(back_populates="user", cascade="all, delete-orphan")
  articles: Mapped[List["Article"]] = relationship(back_populates="author", cascade="all, delete-orphan")
  posts: Mapped[List["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")
  
class VerificationCode(Base):
  __tablename__ = "verification_codes"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
  code: Mapped[str] = mapped_column(String(10), nullable=False)
  type: Mapped[str] = mapped_column(String(50), comment="register, reset_password")
  expire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
  is_used: Mapped[bool] = mapped_column(Boolean, default=False)
  create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))