from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.exceptions import AuthorizationError

# Repositories
from app.repositories.user import UserRepository
from app.repositories.building import BuildingRepository
from app.repositories.complaint import ComplaintRepository
from app.repositories.complaint_history import ComplaintHistoryRepository

from app.repositories.interfaces.user import IUserRepository
from app.repositories.interfaces.building import IBuildingRepository
from app.repositories.interfaces.complaint import IComplaintRepository
from app.repositories.interfaces.complaint_history import IComplaintHistoryRepository

# Services
from app.services.user import UserService
from app.services.auth import AuthService
from app.services.building import BuildingService
from app.services.complaint import ComplaintService

from app.services.interfaces.user import IUserService
from app.services.interfaces.auth import IAuthService
from app.services.interfaces.building import IBuildingService
from app.services.interfaces.complaint import IComplaintService

from app.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# --- Repository Builders ---
def get_user_repo(db: Session = Depends(get_db)) -> IUserRepository:
    return UserRepository(db)

def get_building_repo(db: Session = Depends(get_db)) -> IBuildingRepository:
    return BuildingRepository(db)

def get_complaint_repo(db: Session = Depends(get_db)) -> IComplaintRepository:
    return ComplaintRepository(db)

def get_history_repo(db: Session = Depends(get_db)) -> IComplaintHistoryRepository:
    return ComplaintHistoryRepository(db)

# --- Service Builders ---
def get_user_service(
    repo: IUserRepository = Depends(get_user_repo),
    db: Session = Depends(get_db)
) -> IUserService:
    return UserService(repo, db)

def get_auth_service(
    repo: IUserRepository = Depends(get_user_repo)
) -> IAuthService:
    return AuthService(repo)

def get_building_service(
    repo: IBuildingRepository = Depends(get_building_repo),
    db: Session = Depends(get_db)
) -> IBuildingService:
    return BuildingService(repo, db)

def get_complaint_service(
    complaint_repo: IComplaintRepository = Depends(get_complaint_repo),
    history_repo: IComplaintHistoryRepository = Depends(get_history_repo),
    building_repo: IBuildingRepository = Depends(get_building_repo),
    user_repo: IUserRepository = Depends(get_user_repo),
    db: Session = Depends(get_db)
) -> IComplaintService:
    return ComplaintService(complaint_repo, history_repo, building_repo, user_repo, db)

# --- Authentication & Authorization ---
# (Mock token decoding logic for the scope of this file. In reality, decode JWT here.)
# To safely handle RBAC during this Phase, we'll implement a functional stub 
# that will be fleshed out with python-jose once the JWT core is established.

def get_current_user(token: str = Depends(oauth2_scheme), user_service: IUserService = Depends(get_user_service)) -> User:
    from jose import JWTError, jwt
    from app.core.config import settings
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise AuthorizationError("Could not validate credentials")
    except JWTError:
        raise AuthorizationError("Could not validate credentials")
        
    user = user_service.get_user_by_email(email=email)
    if user is None:
        raise AuthorizationError("User not found")
    if not user.is_active:
        raise AuthorizationError("Inactive user")
    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise AuthorizationError("The user doesn't have enough privileges")
    return current_user

def require_staff_or_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in [UserRole.STAFF, UserRole.ADMIN]:
        raise AuthorizationError("The user doesn't have enough privileges")
    return current_user
