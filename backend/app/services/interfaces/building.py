from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from app.models.building import Building
from app.schemas.building import BuildingCreate, BuildingUpdate

class IBuildingService(ABC):
    @abstractmethod
    def create_building(self, building_create: BuildingCreate) -> Building:
        pass
        
    @abstractmethod
    def get_building(self, building_id: UUID) -> Building:
        pass
        
    @abstractmethod
    def get_all_buildings(self, skip: int = 0, limit: int = 100) -> List[Building]:
        pass
        
    @abstractmethod
    def update_building(self, building_id: UUID, building_update: BuildingUpdate) -> Building:
        pass
