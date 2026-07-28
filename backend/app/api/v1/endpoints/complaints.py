from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate, ComplaintResponse
from app.schemas.common import PaginatedResponse
from app.models.user import User
from app.services.interfaces.complaint import IComplaintService
from app.api.dependencies import get_complaint_service, get_current_user

router = APIRouter()

@router.post("/", response_model=ComplaintResponse)
def create_complaint(
    complaint_in: ComplaintCreate,
    current_user: User = Depends(get_current_user),
    complaint_service: IComplaintService = Depends(get_complaint_service)
):
    """Create a new complaint as a student/user."""
    return complaint_service.create_complaint(complaint_in, current_user)

@router.get("/me", response_model=PaginatedResponse[ComplaintResponse])
def get_my_complaints(
    page: int = 1,
    page_size: int = 10,
    current_user: User = Depends(get_current_user),
    complaint_service: IComplaintService = Depends(get_complaint_service)
):
    """Get all complaints created by the current user."""
    return complaint_service.search_complaints(current_user, page=page, page_size=page_size)

@router.put("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(
    complaint_id: UUID,
    complaint_in: ComplaintUpdate,
    current_user: User = Depends(get_current_user),
    complaint_service: IComplaintService = Depends(get_complaint_service)
):
    """Update a pending complaint (User)."""
    return complaint_service.update_complaint(complaint_id, complaint_in, current_user)

@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(
    complaint_id: UUID,
    current_user: User = Depends(get_current_user),
    complaint_service: IComplaintService = Depends(get_complaint_service)
):
    """Get a specific complaint."""
    return complaint_service.get_complaint(complaint_id, current_user)
