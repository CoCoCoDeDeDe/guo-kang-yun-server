# app\schemas\knowledge.py
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.models.knowledge import PestCategoryEnum

# --- PreventionScheme Schemas ---
class PreventionSchemeBase(BaseModel):
    pesticide_name: str = Field(..., max_length=100)
    recommended_dosage: Optional[str] = Field(None, max_length=100)
    application_time: Optional[str] = Field(None, max_length=100)
    operation_spec: Optional[str] = None

class PreventionSchemeCreate(PreventionSchemeBase):
    pest_id: int

class PreventionSchemeResponse(PreventionSchemeBase):
    id: int
    pest_id: int

    model_config = ConfigDict(from_attributes=True)

# --- PestInfo Schemas ---
class PestInfoBase(BaseModel):
    name: str = Field(..., max_length=100)
    category: PestCategoryEnum
    affected_part: Optional[str] = Field(None, max_length=100)
    symptom_description: Optional[str] = None
    peak_season: Optional[str] = Field(None, max_length=100)
    typical_image: Optional[str] = Field(None, max_length=255)

class PestInfoCreate(PestInfoBase):
    pass

class PestInfoUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    category: Optional[PestCategoryEnum] = None
    affected_part: Optional[str] = Field(None, max_length=100)
    symptom_description: Optional[str] = None
    peak_season: Optional[str] = Field(None, max_length=100)
    typical_image: Optional[str] = Field(None, max_length=255)

class PestInfoResponse(PestInfoBase):
    id: int
    # 嵌套显示关联的防治方案
    prevention_schemes: List[PreventionSchemeResponse] = []

    model_config = ConfigDict(from_attributes=True)