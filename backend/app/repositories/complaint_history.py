import logging
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, desc
from sqlalchemy.exc import SQLAlchemyError

from app.models.complaint import ComplaintHistory
from app.repositories.base import BaseRepository
from app.repositories.interfaces.complaint_history import IComplaintHistoryRepository
from app.core.exceptions import DatabaseError

logger = logging.getLogger(__name__)

class ComplaintHistoryRepository(BaseRepository[ComplaintHistory], IComplaintHistoryRepository):
    """
    Concrete implementation of the ComplaintHistory Repository.
    """
    def __init__(self, db_session: Session):
        super().__init__(model=ComplaintHistory, db_session=db_session)

    def get_history_for_complaint(self, complaint_id: UUID, include_deleted: bool = False) -> List[ComplaintHistory]:
        stmt = (
            select(ComplaintHistory)
            .where(ComplaintHistory.complaint_id == complaint_id)
            .order_by(desc(ComplaintHistory.created_at))
            .options(joinedload(ComplaintHistory.updater))
        )
        
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Error fetching history for complaint {complaint_id}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")
