import logging
from typing import Generic, TypeVar, Type, Optional, List, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError, SQLAlchemyError

from app.database.database import Base
from app.core.exceptions import NotFoundError, IntegrityError, DatabaseError

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Generic Base Repository providing standard CRUD operations.
    Transaction management (commit/rollback) is delegated to the Service layer.
    """
    def __init__(self, model: Type[ModelType], db_session: Session):
        self.model = model
        self.db_session = db_session

    def get(self, id: UUID) -> Optional[ModelType]:
        try:
            stmt = select(self.model).where(self.model.id == id)  # type: ignore[attr-defined]
            result = self.db_session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching {self.model.__name__} by id {id}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def get_by_id(self, id: UUID) -> ModelType:
        obj = self.get(id)
        if not obj:
            raise NotFoundError(entity_name=self.model.__name__, entity_id=str(id))
        return obj

    def list(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        try:
            stmt = select(self.model).offset(skip).limit(limit)
            result = self.db_session.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Error listing {self.model.__name__}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def create(self, **kwargs: Any) -> ModelType:
        obj = self.model(**kwargs)
        self.db_session.add(obj)
        try:
            self.db_session.flush()
            self.db_session.refresh(obj)
            return obj
        except SQLAlchemyIntegrityError as e:
            logger.error(f"Integrity error creating {self.model.__name__}: {e}")
            raise IntegrityError(f"Integrity Error: {str(e)}")
        except SQLAlchemyError as e:
            logger.error(f"Database error creating {self.model.__name__}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def update(self, db_obj: ModelType, **kwargs: Any) -> ModelType:
        for field, value in kwargs.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)
                
        self.db_session.add(db_obj)
        try:
            self.db_session.flush()
            self.db_session.refresh(db_obj)
            return db_obj
        except SQLAlchemyIntegrityError as e:
            logger.error(f"Integrity error updating {self.model.__name__}: {e}")
            raise IntegrityError(f"Integrity Error: {str(e)}")
        except SQLAlchemyError as e:
            logger.error(f"Database error updating {self.model.__name__}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def delete(self, id: UUID) -> None:
        obj = self.get_by_id(id)
        try:
            self.db_session.delete(obj)
            self.db_session.flush()
        except SQLAlchemyIntegrityError as e:
            logger.error(f"Integrity error deleting {self.model.__name__}: {e}")
            raise IntegrityError(f"Integrity Error: {str(e)}")
        except SQLAlchemyError as e:
            logger.error(f"Database error deleting {self.model.__name__}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def soft_delete(self, id: UUID) -> ModelType:
        obj = self.get_by_id(id)
        if not hasattr(obj, 'is_deleted'):
            logger.error(f"soft_delete called on {self.model.__name__} which lacks 'is_deleted' attribute.")
            raise NotImplementedError(f"Model {self.model.__name__} does not support soft deletion.")
        
        setattr(obj, 'is_deleted', True)
        self.db_session.add(obj)
        try:
            self.db_session.flush()
            self.db_session.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            logger.error(f"Database error soft deleting {self.model.__name__}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def count(self) -> int:
        try:
            stmt = select(func.count()).select_from(self.model)
            result = self.db_session.execute(stmt)
            return result.scalar_one()
        except SQLAlchemyError as e:
            logger.error(f"Error counting {self.model.__name__}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def exists(self, id: UUID) -> bool:
        try:
            stmt = select(self.model.id).where(self.model.id == id)  # type: ignore[attr-defined]
            result = self.db_session.execute(stmt)
            return result.scalar_one_or_none() is not None
        except SQLAlchemyError as e:
            logger.error(f"Error checking existence for {self.model.__name__}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")
