from typing import Dict, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.complaint import Complaint, ComplaintHistory
from app.models.user import User, UserRole
from app.models.enums import ComplaintStatus
from app.schemas.complaint import (
    ComplaintCreate, 
    ComplaintUpdate, 
    ComplaintStatusUpdate, 
    ComplaintAssign
)
from app.schemas.common import PaginatedResponse
from app.services.interfaces.complaint import IComplaintService
from app.repositories.interfaces.complaint import IComplaintRepository
from app.repositories.interfaces.complaint_history import IComplaintHistoryRepository
from app.repositories.interfaces.building import IBuildingRepository
from app.repositories.interfaces.user import IUserRepository
from app.core.exceptions import AuthorizationError, ConflictError

class ComplaintService(IComplaintService):
    def __init__(
        self, 
        complaint_repo: IComplaintRepository,
        history_repo: IComplaintHistoryRepository,
        building_repo: IBuildingRepository,
        user_repo: IUserRepository,
        db_session: Session
    ):
        self.complaint_repo = complaint_repo
        self.history_repo = history_repo
        self.building_repo = building_repo
        self.user_repo = user_repo
        self.db_session = db_session

    def create_complaint(self, complaint_in: ComplaintCreate, current_user: User) -> Complaint:
        # Validate building exists
        self.building_repo.get_by_id(complaint_in.building_id)
        
        complaint_data = complaint_in.model_dump()
        complaint_data["reported_by"] = current_user.id
        complaint_data["status"] = ComplaintStatus.PENDING
        
        complaint = self.complaint_repo.create(**complaint_data)
        
        # Log initial creation history
        self.history_repo.create(
            complaint_id=complaint.id,
            old_status=None,
            new_status=ComplaintStatus.PENDING,
            remarks="Complaint reported.",
            updated_by=current_user.id
        )
        
        self.db_session.commit()
        return complaint

    def get_complaint(self, complaint_id: UUID, current_user: User) -> Complaint:
        complaint = self.complaint_repo.get_by_id(complaint_id)
        
        # Enforce RBAC for viewing
        if current_user.role == UserRole.STUDENT and complaint.reported_by != current_user.id:
            raise AuthorizationError("You do not have permission to view this complaint.")
        if current_user.role == UserRole.STAFF and complaint.assigned_to != current_user.id:
            raise AuthorizationError("You do not have permission to view this complaint.")
            
        return complaint

    def search_complaints(self, current_user: User, page: int = 1, page_size: int = 10, **filters: Any) -> PaginatedResponse[Complaint]:
        # Enforce RBAC filtering natively in the query
        if current_user.role == UserRole.STUDENT:
            filters["reported_by"] = current_user.id
        elif current_user.role == UserRole.STAFF:
            filters["assigned_to"] = current_user.id
            
        items, total = self.complaint_repo.search_complaints(
            page=page, 
            page_size=page_size, 
            **filters
        )
        
        import math
        total_pages = math.ceil(total / page_size) if page_size > 0 else 0
        return PaginatedResponse(
            items=items,
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1
        )

    def update_complaint(self, complaint_id: UUID, complaint_in: ComplaintUpdate, current_user: User) -> Complaint:
        complaint = self.get_complaint(complaint_id, current_user)
        
        if complaint.status != ComplaintStatus.PENDING:
            raise ConflictError("You can only edit PENDING complaints.")
            
        if complaint_in.building_id:
            self.building_repo.get_by_id(complaint_in.building_id)
            
        updated = self.complaint_repo.update(complaint, **complaint_in.model_dump(exclude_unset=True))
        self.db_session.commit()
        return updated

    def update_status(self, complaint_id: UUID, status_update: ComplaintStatusUpdate, current_user: User) -> Complaint:
        if current_user.role == UserRole.STUDENT:
            raise AuthorizationError("Students cannot update complaint statuses.")
            
        complaint = self.get_complaint(complaint_id, current_user)
        old_status = complaint.status
        new_status = status_update.status
        
        if old_status == new_status:
            return complaint
            
        update_data: Dict[str, Any] = {"status": new_status}
        
        if new_status == ComplaintStatus.COMPLETED:
            update_data["resolved_at"] = datetime.now()
            if status_update.completion_image_url:
                update_data["completion_image_url"] = status_update.completion_image_url
                
        updated = self.complaint_repo.update(complaint, **update_data)
        
        # Log transition
        self.history_repo.create(
            complaint_id=complaint.id,
            old_status=old_status,
            new_status=new_status,
            remarks=status_update.remarks,
            updated_by=current_user.id
        )
        
        self.db_session.commit()
        return updated

    def assign_complaint(self, complaint_id: UUID, assign_data: ComplaintAssign, current_user: User) -> Complaint:
        if current_user.role != UserRole.ADMIN:
            raise AuthorizationError("Only administrators can assign complaints.")
            
        complaint = self.complaint_repo.get_by_id(complaint_id)
        
        # Ensure assignee is valid and is STAFF
        assignee = self.user_repo.get_by_id(assign_data.assigned_to)
        if assignee.role != UserRole.STAFF:
            raise ConflictError("Complaints can only be assigned to STAFF members.")
            
        old_status = complaint.status
        update_data: Dict[str, Any] = {"assigned_to": assignee.id}
        
        # Automatically transition to IN_PROGRESS if currently PENDING
        if complaint.status == ComplaintStatus.PENDING:
            update_data["status"] = ComplaintStatus.IN_PROGRESS
            
        updated = self.complaint_repo.update(complaint, **update_data)
        
        # If status changed, log it
        if old_status != updated.status:
            self.history_repo.create(
                complaint_id=complaint.id,
                old_status=old_status,
                new_status=updated.status,
                remarks=f"Assigned to {assignee.full_name}",
                updated_by=current_user.id
            )
            
        self.db_session.commit()
        return updated

    def soft_delete_complaint(self, complaint_id: UUID, current_user: User) -> None:
        if current_user.role != UserRole.ADMIN:
            raise AuthorizationError("Only administrators can delete complaints.")
            
        self.complaint_repo.soft_delete(complaint_id)
        self.db_session.commit()

    def get_dashboard_stats(self, current_user: User) -> Dict[str, Any]:
        return {
            "status_counts": self.complaint_repo.get_status_counts(),
            "priority_counts": self.complaint_repo.get_priority_counts(),
            "category_counts": self.complaint_repo.get_category_counts(),
            "building_counts": self.complaint_repo.get_building_counts(),
            "recent": self.complaint_repo.get_recent_complaints(limit=5),
            "monthly_trend": self.complaint_repo.get_monthly_trend(months=6)
        }
