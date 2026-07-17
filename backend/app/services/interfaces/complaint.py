from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from uuid import UUID

from app.models.complaint import Complaint
from app.models.user import User
from app.schemas.complaint import (
    ComplaintCreate, 
    ComplaintUpdate, 
    ComplaintStatusUpdate, 
    ComplaintAssign
)
from app.schemas.common import PaginatedResponse

class IComplaintService(ABC):
    @abstractmethod
    def create_complaint(self, complaint_in: ComplaintCreate, current_user: User) -> Complaint:
        pass
        
    @abstractmethod
    def get_complaint(self, complaint_id: UUID, current_user: User) -> Complaint:
        pass
        
    @abstractmethod
    def search_complaints(self, current_user: User, page: int = 1, page_size: int = 10, **filters: Any) -> PaginatedResponse[Complaint]:
        pass
        
    @abstractmethod
    def update_complaint(self, complaint_id: UUID, complaint_in: ComplaintUpdate, current_user: User) -> Complaint:
        """Student updates their own pending complaint."""
        pass
        
    @abstractmethod
    def update_status(self, complaint_id: UUID, status_update: ComplaintStatusUpdate, current_user: User) -> Complaint:
        """Staff/Admin updates status (and auto-logs history)."""
        pass
        
    @abstractmethod
    def assign_complaint(self, complaint_id: UUID, assign_data: ComplaintAssign, current_user: User) -> Complaint:
        """Admin assigns a complaint to a staff member."""
        pass
        
    @abstractmethod
    def soft_delete_complaint(self, complaint_id: UUID, current_user: User) -> None:
        """Admin soft-deletes a complaint."""
        pass
        
    @abstractmethod
    def get_dashboard_stats(self, current_user: User) -> Dict[str, Any]:
        """Returns aggregated dashboard statistics."""
        pass
