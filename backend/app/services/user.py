from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.interfaces.user import IUserService
from app.repositories.interfaces.user import IUserRepository
from app.core.security import get_password_hash
from app.core.exceptions import ConflictError

class UserService(IUserService):
    def __init__(self, user_repo: IUserRepository, db_session: Session):
        self.user_repo = user_repo
        self.db_session = db_session

    def get_user_by_id(self, user_id: UUID) -> User:
        return self.user_repo.get_by_id(user_id)
        
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repo.get_by_email(email)
        
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.user_repo.get_all(skip=skip, limit=limit)
        
    def create_user(self, user_create: UserCreate) -> User:
        # Check if email is unique
        existing_user = self.user_repo.get_by_email(user_create.email)
        if existing_user:
            raise ConflictError("A user with this email already exists.")
            
        hashed_password = get_password_hash(user_create.password)
        
        user_data = user_create.model_dump(exclude={"password"})
        user_data["hashed_password"] = hashed_password
        
        user = self.user_repo.create(**user_data)
        self.db_session.commit()
        return user

    def update_user(self, user_id: UUID, user_update: UserUpdate) -> User:
        user = self.user_repo.get_by_id(user_id)
        
        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
            
        updated_user = self.user_repo.update(user, **update_data)
        self.db_session.commit()
        return updated_user
