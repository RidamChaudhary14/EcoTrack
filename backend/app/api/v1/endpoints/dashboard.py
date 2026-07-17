from typing import Dict, Any
from fastapi import APIRouter, Depends
from app.models.user import User
from app.services.interfaces.complaint import IComplaintService
from app.api.dependencies import get_complaint_service, require_admin

router = APIRouter()

@router.get("/stats", response_model=Dict[str, Any])
def get_dashboard_stats(
    current_admin: User = Depends(require_admin),
    complaint_service: IComplaintService = Depends(get_complaint_service)
):
    """Admin: Fetch aggregate dashboard statistics."""
    return complaint_service.get_dashboard_stats(current_admin)
