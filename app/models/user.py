# app\models\user.py
# Outer
import enum
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Mine
from app.db.database import Base

# class RoleEnum(int, enum.Enum): # A
# class RoleEnum(enum.Enum): # B 不支持 RoleEnum(数字)
class RoleEnum(enum.IntEnum): # C 等效 A
  FARMER = 0
  EXPERT = 1
  ADMIN = 2
  
print(RoleEnum)
print(type(RoleEnum))
print(RoleEnum.ADMIN)
print(type(RoleEnum.ADMIN))
print(RoleEnum.ADMIN.name)
print(RoleEnum.ADMIN.value)
print(RoleEnum(0))
# print(RoleEnum(3)) # 运行后报错