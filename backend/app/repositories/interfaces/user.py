from abc import abstractmethod
from typing import Optional
from app.repositories.interfaces.base import IBaseRepository
from app.models.user import User

class IUserRepository(IBaseRepository[User]):
    """
    Interface for User repository operations.
    Extends generic IBaseRepository with domain-specific user lookups.
    """
    
    @abstractmethod
    def get_by_email(self, email: str, include_deleted: bool = False) -> Optional[User]:
        """
        Fetch a user by their unique email address.
        Used primarily during authentication.
        """
        pass
