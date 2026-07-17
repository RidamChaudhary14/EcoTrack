import logging
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.building import Building
from app.repositories.base import BaseRepository
from app.repositories.interfaces.building import IBuildingRepository
from app.core.exceptions import DatabaseError

logger = logging.getLogger(__name__)

class BuildingRepository(BaseRepository[Building], IBuildingRepository):
    """
    Concrete implementation of the Building Repository.
    """
    def __init__(self, db_session: Session):
        super().__init__(model=Building, db_session=db_session)

    def get_by_name(self, name: str, include_deleted: bool = False) -> Optional[Building]:
        stmt = select(Building).where(Building.name == name)
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching Building by name {name}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def get_by_code(self, code: str, include_deleted: bool = False) -> Optional[Building]:
        stmt = select(Building).where(Building.code == code)
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching Building by code {code}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")
