import logging
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.user import User
from app.repositories.base import BaseRepository
from app.repositories.interfaces.user import IUserRepository
from app.core.exceptions import DatabaseError

logger = logging.getLogger(__name__)

class UserRepository(BaseRepository[User], IUserRepository):
    """
    Concrete implementation of the User Repository.
    """
    def __init__(self, db_session: Session):
        super().__init__(model=User, db_session=db_session)

    def get_by_email(self, email: str, include_deleted: bool = False) -> Optional[User]:
        """
        Retrieves a user by email.
        """
        stmt = select(User).where(User.email == email)
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching User by email {email}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")
