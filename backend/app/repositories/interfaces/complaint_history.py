from abc import abstractmethod
from typing import List
from uuid import UUID
from app.repositories.interfaces.base import IBaseRepository
from app.models.complaint import ComplaintHistory

class IComplaintHistoryRepository(IBaseRepository[ComplaintHistory]):
    """
    Interface for ComplaintHistory repository operations (Audit Log).
    """
    
    @abstractmethod
    def get_history_for_complaint(self, complaint_id: UUID, include_deleted: bool = False) -> List[ComplaintHistory]:
        """Fetch the chronologically ordered audit trail for a specific complaint."""
        pass
