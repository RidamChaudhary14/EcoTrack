from fastapi import APIRouter
from app.api.v1.endpoints import auth, buildings, complaints, staff, admin, dashboard, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(buildings.router, prefix="/buildings", tags=["buildings"])
api_router.include_router(complaints.router, prefix="/complaints", tags=["complaints"])
api_router.include_router(staff.router, prefix="/staff", tags=["staff"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
