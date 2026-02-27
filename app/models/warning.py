# app\models\warning.py
import enum
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class WarningLevelEnum(str, enum.Enum):
  NORMAL = "普通"
  URGENT = "紧急"

class WarningMessage(Base):
  __tablename__ = "warning_messages"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  level: Mapped[WarningLevelEnum] = mapped_column(Enum(WarningLevelEnum), default=WarningLevelEnum.NORMAL)
  affected_scope: Mapped[str] = mapped_column(String(255))
  prevention_measures: Mapped[Text] = mapped_column(Text, nullable=False)
  publish_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
  expire_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)