from sqlalchemy.orm import Session
from app.models.user import User
from app.services.interfaces.auth import IAuthService
from app.repositories.interfaces.user import IUserRepository
from app.core.security import verify_password
from app.core.exceptions import AuthorizationError

class AuthService(IAuthService):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise AuthorizationError("Incorrect email or password")
            
        if not verify_password(password, str(user.hashed_password)):
            raise AuthorizationError("Incorrect email or password")
            
        if not user.is_active:
            raise AuthorizationError("Inactive user")
            
        return user
