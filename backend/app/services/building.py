from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.building import Building
from app.schemas.building import BuildingCreate, BuildingUpdate
from app.services.interfaces.building import IBuildingService
from app.repositories.interfaces.building import IBuildingRepository
from app.core.exceptions import ConflictError

class BuildingService(IBuildingService):
    def __init__(self, building_repo: IBuildingRepository, db_session: Session):
        self.building_repo = building_repo
        self.db_session = db_session

    def create_building(self, building_create: BuildingCreate) -> Building:
        # Enforce unique code and name
        if self.building_repo.get_by_code(building_create.code):
            raise ConflictError("A building with this code already exists.")
        if self.building_repo.get_by_name(building_create.name):
            raise ConflictError("A building with this name already exists.")
            
        building = self.building_repo.create(**building_create.model_dump())
        self.db_session.commit()
        return building
        
    def get_building(self, building_id: UUID) -> Building:
        return self.building_repo.get_by_id(building_id)
        
    def get_all_buildings(self, skip: int = 0, limit: int = 100) -> List[Building]:
        return self.building_repo.get_all(skip=skip, limit=limit)
        
    def update_building(self, building_id: UUID, building_update: BuildingUpdate) -> Building:
        building = self.building_repo.get_by_id(building_id)
        
        # Enforce unique code and name on update if they changed
        if building_update.code and building_update.code != building.code:
            if self.building_repo.get_by_code(building_update.code):
                raise ConflictError("A building with this code already exists.")
                
        if building_update.name and building_update.name != building.name:
            if self.building_repo.get_by_name(building_update.name):
                raise ConflictError("A building with this name already exists.")
                
        updated_building = self.building_repo.update(building, **building_update.model_dump(exclude_unset=True))
        self.db_session.commit()
        return updated_building
