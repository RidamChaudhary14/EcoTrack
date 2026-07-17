from uuid import UUID
from fastapi import APIRouter, Depends
from app.schemas.complaint import ComplaintStatusUpdate, ComplaintResponse
from app.schemas.common import PaginatedResponse
from app.models.user import User
from app.services.interfaces.complaint import IComplaintService
from app.api.dependencies import get_complaint_service, require_staff_or_admin

router = APIRouter()

@router.get("/complaints", response_model=PaginatedResponse[ComplaintResponse])
def get_assigned_complaints(
    page: int = 1,
    page_size: int = 10,
    current_staff: User = Depends(require_staff_or_admin),
    complaint_service: IComplaintService = Depends(get_complaint_service)
):
    """Staff: Get all assigned complaints."""
    return complaint_service.search_complaints(current_staff, page=page, page_size=page_size)

@router.patch("/complaints/{complaint_id}/status", response_model=ComplaintResponse)
def update_complaint_status(
    complaint_id: UUID,
    status_update: ComplaintStatusUpdate,
    current_staff: User = Depends(require_staff_or_admin),
    complaint_service: IComplaintService = Depends(get_complaint_service)
):
    """Staff: Update the status of an assigned complaint."""
    return complaint_service.update_status(complaint_id, status_update, current_staff)
