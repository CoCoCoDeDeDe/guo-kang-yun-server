# app\schemas\warning.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.models.warning import WarningLevelEnum

class WarningMessageBase(BaseModel):
    level: WarningLevelEnum = WarningLevelEnum.NORMAL
    affected_scope: str = Field(..., max_length=255)
    prevention_measures: str
    expire_time: datetime

class WarningMessageCreate(WarningMessageBase):
    pass

class WarningMessageUpdate(BaseModel):
    level: Optional[WarningLevelEnum] = None
    affected_scope: Optional[str] = Field(None, max_length=255)
    prevention_measures: Optional[str] = None
    expire_time: Optional[datetime] = None

class WarningMessageResponse(WarningMessageBase):
    id: int
    publish_time: datetime

    model_config = ConfigDict(from_attributes=True)