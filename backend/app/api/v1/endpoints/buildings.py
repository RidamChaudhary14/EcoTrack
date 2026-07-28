from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from app.schemas.building import BuildingCreate, BuildingUpdate, BuildingResponse
from app.services.interfaces.building import IBuildingService
from app.api.dependencies import get_building_service, require_admin

router = APIRouter()

@router.get("/", response_model=List[BuildingResponse])
def get_buildings(
    skip: int = 0,
    limit: int = 100,
    building_service: IBuildingService = Depends(get_building_service)
):
    """Retrieve all buildings."""
    return building_service.get_all_buildings(skip=skip, limit=limit)

@router.post("/", response_model=BuildingResponse)
def create_building(
    building_in: BuildingCreate,
    building_service: IBuildingService = Depends(get_building_service),
    current_admin = Depends(require_admin)
):
    """Create a new building. Requires Admin."""
    return building_service.create_building(building_in)

@router.put("/{building_id}", response_model=BuildingResponse)
def update_building(
    building_id: UUID,
    building_in: BuildingUpdate,
    building_service: IBuildingService = Depends(get_building_service),
    current_admin = Depends(require_admin)
):
    """Update a building. Requires Admin."""
    return building_service.update_building(building_id, building_in)
