import logging
from typing import List, Tuple, Dict, Any, Optional
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select, func, desc, asc, or_
from sqlalchemy.exc import SQLAlchemyError

from app.models.complaint import Complaint
from app.models.building import Building
from app.repositories.base import BaseRepository
from app.repositories.interfaces.complaint import IComplaintRepository
from app.core.exceptions import DatabaseError

logger = logging.getLogger(__name__)

class ComplaintRepository(BaseRepository[Complaint], IComplaintRepository):
    """
    Concrete implementation of the Complaint Repository.
    Handles dynamic search queries and aggregate reporting.
    """
    def __init__(self, db_session: Session):
        super().__init__(model=Complaint, db_session=db_session)

    def _build_search_query(self, include_deleted: bool, filters: Dict[str, Any]) -> Any:
        stmt = select(Complaint)
        
        # Handle keyword search which requires a join on Building
        keyword = filters.pop("keyword", None)
        if keyword:
            stmt = stmt.outerjoin(Building).where(
                or_(
                    Complaint.title.ilike(f"%{keyword}%"),
                    Complaint.description.ilike(f"%{keyword}%"),
                    Complaint.location_description.ilike(f"%{keyword}%"),
                    Building.name.ilike(f"%{keyword}%")
                )
            )

        stmt = self._apply_soft_delete_filter(stmt, include_deleted)

        # Handle range filters
        created_after = filters.pop("created_after", None)
        if created_after:
            stmt = stmt.where(Complaint.created_at >= created_after)
            
        created_before = filters.pop("created_before", None)
        if created_before:
            stmt = stmt.where(Complaint.created_at <= created_before)

        # Handle exact match filters
        for key, value in filters.items():
            if hasattr(Complaint, key) and value is not None:
                stmt = stmt.where(getattr(Complaint, key) == value)

        return stmt

    def search_complaints(
        self,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        include_deleted: bool = False,
        **filters: Any
    ) -> Tuple[List[Complaint], int]:
        
        base_stmt = self._build_search_query(include_deleted, filters)
        
        try:
            # 1. Get total count
            count_stmt = select(func.count()).select_from(base_stmt.subquery())
            total = self.db_session.execute(count_stmt).scalar_one()

            # 2. Get paginated and sorted items
            stmt = base_stmt
            
            # Eager load relationships for list views (selectin for One-to-Many equivalent or reducing joins)
            # joinedload for building because it's Many-to-One
            stmt = stmt.options(
                joinedload(Complaint.building),
                selectinload(Complaint.reporter),
                selectinload(Complaint.assignee)
            )

            # Apply sorting
            if sort_by == "building":
                # Special handling for sorting by building name
                if not "keyword" in filters: # if we didn't already join building
                    stmt = stmt.outerjoin(Building)
                order_col = Building.name
            elif hasattr(Complaint, sort_by):
                order_col = getattr(Complaint, sort_by)
            else:
                order_col = Complaint.created_at

            stmt = stmt.order_by(desc(order_col) if sort_order.lower() == "desc" else asc(order_col))

            # Apply pagination
            skip = (page - 1) * page_size
            stmt = stmt.offset(skip).limit(page_size)

            items = list(self.db_session.execute(stmt).scalars().all())
            return items, total
            
        except SQLAlchemyError as e:
            logger.error(f"Error searching complaints: {e}")
            raise DatabaseError(f"Database error occurred during search: {str(e)}")

    def get_status_counts(self, include_deleted: bool = False) -> Dict[str, int]:
        stmt = select(Complaint.status, func.count(Complaint.id)).group_by(Complaint.status)
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt).all()
            return {status.name if hasattr(status, 'name') else str(status): count for status, count in result}
        except SQLAlchemyError as e:
            logger.error(f"Error fetching status counts: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def get_priority_counts(self, include_deleted: bool = False) -> Dict[str, int]:
        stmt = select(Complaint.priority, func.count(Complaint.id)).group_by(Complaint.priority)
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt).all()
            return {priority.name if hasattr(priority, 'name') else str(priority): count for priority, count in result}
        except SQLAlchemyError as e:
            logger.error(f"Error fetching priority counts: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")
            
    def get_category_counts(self, include_deleted: bool = False) -> Dict[str, int]:
        stmt = select(Complaint.category, func.count(Complaint.id)).group_by(Complaint.category)
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt).all()
            return {category.name if hasattr(category, 'name') else str(category): count for category, count in result}
        except SQLAlchemyError as e:
            logger.error(f"Error fetching category counts: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def get_building_counts(self, include_deleted: bool = False) -> List[Dict[str, Any]]:
        stmt = (
            select(Building.name, func.count(Complaint.id))
            .join(Complaint, Complaint.building_id == Building.id)
            .group_by(Building.name)
        )
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt).all()
            return [{"building": name, "count": count} for name, count in result]
        except SQLAlchemyError as e:
            logger.error(f"Error fetching building counts: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def get_monthly_trend(self, months: int = 6, include_deleted: bool = False) -> List[Dict[str, Any]]:
        # A basic approach to group by month. Note: dialect specific truncations might be needed for perfect accuracy,
        # but func.date_trunc('month', ...) is standard for Postgres.
        stmt = (
            select(
                func.date_trunc('month', Complaint.created_at).label('month'),
                func.count(Complaint.id).label('count')
            )
            .group_by('month')
            .order_by(desc('month'))
            .limit(months)
        )
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt).all()
            # Sort ascending for chronological trend
            trend = [{"month": row.month.strftime("%Y-%m"), "count": row.count} for row in result]
            return sorted(trend, key=lambda x: x["month"])
        except SQLAlchemyError as e:
            logger.error(f"Error fetching monthly trend: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def get_recent_complaints(self, limit: int = 5, include_deleted: bool = False) -> List[Complaint]:
        stmt = select(Complaint).order_by(desc(Complaint.created_at)).limit(limit)
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        stmt = stmt.options(
            joinedload(Complaint.building),
            selectinload(Complaint.reporter)
        )
        
        try:
            result = self.db_session.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Error fetching recent complaints: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")
