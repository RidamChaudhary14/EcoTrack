from abc import abstractmethod
from typing import Optional
from app.repositories.interfaces.base import IBaseRepository
from app.models.building import Building

class IBuildingRepository(IBaseRepository[Building]):
    """
    Interface for Building repository operations.
    """
    
    @abstractmethod
    def get_by_name(self, name: str, include_deleted: bool = False) -> Optional[Building]:
        """Fetch a building by its exact name."""
        pass

    @abstractmethod
    def get_by_code(self, code: str, include_deleted: bool = False) -> Optional[Building]:
        """Fetch a building by its unique code."""
        pass
