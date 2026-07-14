from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from app.models.enums import ComplaintStatus, Priority, WasteType, ComplaintCategory

class ComplaintHistoryBase(BaseModel):
    old_status: Optional[ComplaintStatus] = Field(None, description="Previous status")
    new_status: ComplaintStatus = Field(..., description="New status")
    remarks: Optional[str] = Field(None, description="Remarks for the status change")

class ComplaintHistoryResponse(ComplaintHistoryBase):
    id: UUID
    complaint_id: UUID
    updated_by: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ComplaintBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100, description="Title of the complaint")
    description: str = Field(..., min_length=10, max_length=500, description="Detailed description")
    category: ComplaintCategory = Field(..., description="Category of the complaint")
    waste_type: WasteType = Field(..., description="Type of waste involved")
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level")
    
    building_id: UUID = Field(..., description="ID of the building")
    floor: Optional[str] = Field(None, description="Floor number/name", max_length=50)
    room: Optional[str] = Field(None, description="Room number/name", max_length=50)
    landmark: Optional[str] = Field(None, description="Nearby landmark", max_length=100)
    location_description: Optional[str] = Field(None, description="Additional location details")
    
    image_url: Optional[str] = Field(None, description="URL of the uploaded image")

class ComplaintCreate(ComplaintBase):
    """Schema for a student creating a complaint"""
    pass

class ComplaintUpdate(BaseModel):
    """Schema for a student updating a PENDING complaint"""
    title: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, min_length=10, max_length=500)
    category: Optional[ComplaintCategory] = None
    waste_type: Optional[WasteType] = None
    priority: Optional[Priority] = None
    
    building_id: Optional[UUID] = None
    floor: Optional[str] = Field(None, max_length=50)
    room: Optional[str] = Field(None, max_length=50)
    landmark: Optional[str] = Field(None, max_length=100)
    location_description: Optional[str] = None
    
    image_url: Optional[str] = None

class ComplaintStatusUpdate(BaseModel):
    """Schema for staff updating a complaint's status"""
    status: ComplaintStatus = Field(..., description="New status to set")
    remarks: Optional[str] = Field(None, description="Optional remarks for the history log")
    completion_image_url: Optional[str] = Field(None, description="Optional image URL when resolving")

class ComplaintAssign(BaseModel):
    """Schema for admins assigning a complaint"""
    assigned_to: UUID = Field(..., description="User ID of the staff member to assign")

class ComplaintResponse(ComplaintBase):
    id: UUID
    status: ComplaintStatus
    reported_by: UUID
    assigned_to: Optional[UUID]
    completion_image_url: Optional[str]
    is_deleted: bool
    resolved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    history: List[ComplaintHistoryResponse] = Field(default_factory=list, description="Audit trail of status changes")
    
    model_config = ConfigDict(from_attributes=True)
