from abc import abstractmethod
from typing import List, Tuple, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from app.repositories.interfaces.base import IBaseRepository
from app.models.complaint import Complaint

class IComplaintRepository(IBaseRepository[Complaint]):
    """
    Interface for Complaint repository operations.
    Supports complex querying, pagination, and dashboard aggregations.
    """
    
    @abstractmethod
    def search_complaints(
        self,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        include_deleted: bool = False,
        **filters: Any
    ) -> Tuple[List[Complaint], int]:
        """
        Search complaints dynamically.
        Returns a tuple of (items, total_count) for pagination.
        Filters support status, priority, category, waste_type, building_id, 
        reported_by, assigned_to, created_after, created_before, keyword.
        """
        pass
        
    @abstractmethod
    def get_status_counts(self, include_deleted: bool = False) -> Dict[str, int]:
        """Returns the count of complaints grouped by status."""
        pass

    @abstractmethod
    def get_priority_counts(self, include_deleted: bool = False) -> Dict[str, int]:
        """Returns the count of complaints grouped by priority."""
        pass
        
    @abstractmethod
    def get_category_counts(self, include_deleted: bool = False) -> Dict[str, int]:
        """Returns the count of complaints grouped by category."""
        pass

    @abstractmethod
    def get_building_counts(self, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """Returns the count of complaints grouped by building name."""
        pass
        
    @abstractmethod
    def get_monthly_trend(self, months: int = 6, include_deleted: bool = False) -> List[Dict[str, Any]]:
        """Returns a month-by-month trend of complaint creation."""
        pass
        
    @abstractmethod
    def get_recent_complaints(self, limit: int = 5, include_deleted: bool = False) -> List[Complaint]:
        """Returns the most recent complaints, eager-loading relationships."""
        pass
