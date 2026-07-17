import logging
from typing import Generic, TypeVar, Type, Optional, List, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError, SQLAlchemyError

from app.database.database import Base
from app.core.exceptions import NotFoundError, IntegrityError, DatabaseError
from app.repositories.interfaces.base import IBaseRepository

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(IBaseRepository[ModelType]):
    """
    Generic Base Repository implementing standard CRUD operations via SQLAlchemy 2.0.
    """
    def __init__(self, model: Type[ModelType], db_session: Session):
        self.model = model
        self.db_session = db_session

    def _apply_soft_delete_filter(self, stmt: Any, include_deleted: bool) -> Any:
        """Applies soft-delete filtering if the model supports it and include_deleted is False."""
        if not include_deleted and hasattr(self.model, "is_deleted"):
            stmt = stmt.where(self.model.is_deleted == False)
        return stmt

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

    def get_by_id(self, id: UUID, include_deleted: bool = False) -> ModelType:
        stmt = select(self.model).where(self.model.id == id) # type: ignore[attr-defined]
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt)
            obj = result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching {self.model.__name__} by id {id}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")
            
        if not obj:
            raise NotFoundError(entity_name=self.model.__name__, entity_id=str(id))
        return obj

    def get_all(self, skip: int = 0, limit: int = 100, include_deleted: bool = False) -> List[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Error listing {self.model.__name__}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def find_one(self, include_deleted: bool = False, **kwargs: Any) -> Optional[ModelType]:
        stmt = select(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)
        
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Error executing find_one for {self.model.__name__}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def find_many(self, skip: int = 0, limit: int = 100, include_deleted: bool = False, **kwargs: Any) -> List[ModelType]:
        stmt = select(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)
                
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        stmt = stmt.offset(skip).limit(limit)
        
        try:
            result = self.db_session.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError as e:
            logger.error(f"Error executing find_many for {self.model.__name__}: {e}")
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

    def soft_delete(self, id: UUID) -> ModelType:
        obj = self.get_by_id(id, include_deleted=False)
        if not hasattr(obj, 'is_deleted'):
            raise NotImplementedError(f"Model {self.model.__name__} does not support soft deletion.")
        
        return self.update(obj, is_deleted=True)

    def restore(self, id: UUID) -> ModelType:
        # We must explicitly look for deleted records to restore them
        obj = self.get_by_id(id, include_deleted=True)
        if not hasattr(obj, 'is_deleted'):
            raise NotImplementedError(f"Model {self.model.__name__} does not support restoration.")
        
        return self.update(obj, is_deleted=False)

    def hard_delete(self, id: UUID) -> None:
        # We can hard delete a soft-deleted object, so include_deleted=True
        obj = self.get_by_id(id, include_deleted=True)
        try:
            self.db_session.delete(obj)
            self.db_session.flush()
        except SQLAlchemyIntegrityError as e:
            logger.error(f"Integrity error hard deleting {self.model.__name__}: {e}")
            raise IntegrityError(f"Integrity Error: {str(e)}")
        except SQLAlchemyError as e:
            logger.error(f"Database error hard deleting {self.model.__name__}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def exists(self, id: UUID, include_deleted: bool = False) -> bool:
        stmt = select(self.model.id).where(self.model.id == id) # type: ignore[attr-defined]
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt)
            return result.scalar_one_or_none() is not None
        except SQLAlchemyError as e:
            logger.error(f"Error checking existence for {self.model.__name__}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")

    def count(self, include_deleted: bool = False) -> int:
        stmt = select(func.count()).select_from(self.model)
        stmt = self._apply_soft_delete_filter(stmt, include_deleted)
        
        try:
            result = self.db_session.execute(stmt)
            return result.scalar_one()
        except SQLAlchemyError as e:
            logger.error(f"Error counting {self.model.__name__}: {e}")
            raise DatabaseError(f"Database error occurred: {str(e)}")
