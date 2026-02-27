# app\models\knowledge.py
import enum
from typing import List, Optional
from sqlalchemy import String, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class PestCategoryEnum(str, enum.Enum):
  DISEASE = "病害"
  PEST = "虫害"

class PestInfo(Base):
  __tablename__ = "pest_info"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
  category: Mapped[PestCategoryEnum] = mapped_column(Enum(PestCategoryEnum), nullable=False)
  affected_part: Mapped[Optional[str]] = mapped_column(String(100))
  symptom_description: Mapped[Optional[str]] = mapped_column(Text)
  peak_season: Mapped[Optional[str]] = mapped_column(String(100))
  typical_image: Mapped[Optional[str]] = mapped_column(String(255))

  prevention_schemes: Mapped[List["PreventionScheme"]] = relationship(back_populates="pest_info", cascade="all, delete-orphan")

class PreventionScheme(Base):
  __tablename__ = "prevention_schemes"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  pest_id: Mapped[int] = mapped_column(ForeignKey("pest_info.id", ondelete="CASCADE"), nullable=False)
  pesticide_name: Mapped[str] = mapped_column(String(100), nullable=False)
  recommended_dosage: Mapped[Optional[str]] = mapped_column(String(100))
  application_time: Mapped[Optional[str]] = mapped_column(String(100))
  operation_spec: Mapped[Optional[str]] = mapped_column(Text)

  pest_info: Mapped["PestInfo"] = relationship(back_populates="prevention_schemes")