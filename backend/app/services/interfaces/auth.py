from abc import ABC, abstractmethod
from typing import Tuple
from app.models.user import User

class IAuthService(ABC):
    @abstractmethod
    def authenticate_user(self, email: str, password: str) -> User:
        """Verifies credentials and returns User."""
        pass
