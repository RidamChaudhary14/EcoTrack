from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class BuildingBase(BaseModel):
    name: str = Field(..., description="Name of the building", max_length=100)
    code: str = Field(..., description="Unique building code", max_length=20)
    latitude: Optional[float] = Field(None, description="Building latitude")
    longitude: Optional[float] = Field(None, description="Building longitude")
    description: Optional[str] = Field(None, description="Building description", max_length=500)
    is_active: bool = Field(True, description="Whether the building is active")

class BuildingCreate(BuildingBase):
    pass

class BuildingUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the building", max_length=100)
    code: Optional[str] = Field(None, description="Unique building code", max_length=20)
    latitude: Optional[float] = Field(None, description="Building latitude")
    longitude: Optional[float] = Field(None, description="Building longitude")
    description: Optional[str] = Field(None, description="Building description", max_length=500)
    is_active: Optional[bool] = Field(None, description="Whether the building is active")

class BuildingResponse(BuildingBase):
    id: UUID = Field(..., description="Building unique ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)
