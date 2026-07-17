from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class IUserService(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> User:
        pass
        
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass
        
    @abstractmethod
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        pass
        
    @abstractmethod
    def update_user(self, user_id: UUID, user_update: UserUpdate) -> User:
        pass
        
    @abstractmethod
    def create_user(self, user_create: UserCreate) -> User:
        pass
