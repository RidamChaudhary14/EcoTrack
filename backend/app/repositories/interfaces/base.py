from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any
from uuid import UUID
from app.database.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class IBaseRepository(ABC, Generic[ModelType]):
    @abstractmethod
    def create(self, **kwargs: Any) -> ModelType:
        pass

    @abstractmethod
    def get_by_id(self, id: UUID, include_deleted: bool = False) -> ModelType:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100, include_deleted: bool = False) -> List[ModelType]:
        pass

    @abstractmethod
    def find_one(self, include_deleted: bool = False, **kwargs: Any) -> Optional[ModelType]:
        pass

    @abstractmethod
    def find_many(self, skip: int = 0, limit: int = 100, include_deleted: bool = False, **kwargs: Any) -> List[ModelType]:
        pass

    @abstractmethod
    def update(self, db_obj: ModelType, **kwargs: Any) -> ModelType:
        pass

    @abstractmethod
    def soft_delete(self, id: UUID) -> ModelType:
        pass

    @abstractmethod
    def restore(self, id: UUID) -> ModelType:
        pass

    @abstractmethod
    def hard_delete(self, id: UUID) -> None:
        pass

    @abstractmethod
    def exists(self, id: UUID, include_deleted: bool = False) -> bool:
        pass

    @abstractmethod
    def count(self, include_deleted: bool = False) -> int:
        pass
