# app\models\governance.py
import enum
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class GovernanceStatusEnum(str, enum.Enum):
  IN_PROGRESS = "进行中"
  RESOLVED = "已解决"

class GovernanceRecord(Base):
  __tablename__ = "governance_records"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  pest_type: Mapped[str] = mapped_column(String(100), nullable=False)
  found_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
  location: Mapped[Optional[str]] = mapped_column(String(255))
  status: Mapped[GovernanceStatusEnum] = mapped_column(Enum(GovernanceStatusEnum), default=GovernanceStatusEnum.IN_PROGRESS)
  description: Mapped[Optional[str]] = mapped_column(Text)
  photos: Mapped[Optional[list]] = mapped_column(JSONB)

  user: Mapped["User"] = relationship(back_populates="governance_records")