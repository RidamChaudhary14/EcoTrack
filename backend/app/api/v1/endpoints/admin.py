from typing import Optional, Any
from uuid import UUID
from fastapi import APIRouter, Depends
from app.schemas.complaint import ComplaintAssign, ComplaintResponse
from app.schemas.common import PaginatedResponse
from app.models.user import User
from app.services.interfaces.complaint import IComplaintService
from app.api.dependencies import get_complaint_service, require_admin

router = APIRouter()

@router.get("/complaints", response_model=PaginatedResponse[ComplaintResponse])
def get_all_complaints(
    page: int = 1,
    page_size: int = 10,
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    current_admin: User = Depends(require_admin),
    complaint_service: IComplaintService = Depends(get_complaint_service)
):
    """Admin: Get all complaints across the system with filtering."""
    filters = {}
    if keyword: filters["keyword"] = keyword
    if status: filters["status"] = status
    if priority: filters["priority"] = priority
    
    return complaint_service.search_complaints(current_admin, page=page, page_size=page_size, **filters)

@router.patch("/complaints/{complaint_id}/assign", response_model=ComplaintResponse)
def assign_complaint(
    complaint_id: UUID,
    assign_data: ComplaintAssign,
    current_admin: User = Depends(require_admin),
    complaint_service: IComplaintService = Depends(get_complaint_service)
):
    """Admin: Assign a complaint to a staff member."""
    return complaint_service.assign_complaint(complaint_id, assign_data, current_admin)

@router.delete("/complaints/{complaint_id}")
def delete_complaint(
    complaint_id: UUID,
    current_admin: User = Depends(require_admin),
    complaint_service: IComplaintService = Depends(get_complaint_service)
):
    """Admin: Soft delete a complaint."""
    complaint_service.soft_delete_complaint(complaint_id, current_admin)
    return {"message": "Complaint successfully deleted"}
