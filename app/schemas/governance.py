# app\schemas\governance.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.models.governance import GovernanceStatusEnum

class GovernanceRecordBase(BaseModel):
    pest_type: str = Field(..., max_length=100)
    found_time: datetime
    location: Optional[str] = Field(None, max_length=255)
    status: GovernanceStatusEnum = GovernanceStatusEnum.IN_PROGRESS
    description: Optional[str] = None
    photos: Optional[List[str]] = None

class GovernanceRecordCreate(GovernanceRecordBase):
    # 通常用户ID从Token中获取，但在严格模式下也可能需要前端显式传递或在依赖注入时补齐
    user_id: int 

class GovernanceRecordUpdate(BaseModel):
    pest_type: Optional[str] = Field(None, max_length=100)
    found_time: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=255)
    status: Optional[GovernanceStatusEnum] = None
    description: Optional[str] = None
    photos: Optional[List[str]] = None

class GovernanceRecordResponse(GovernanceRecordBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)