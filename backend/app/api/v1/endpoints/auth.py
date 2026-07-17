from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserResponse
from app.services.interfaces.auth import IAuthService
from app.services.interfaces.user import IUserService
from app.api.dependencies import get_auth_service, get_user_service
from app.core.config import settings

# Wait! The token schema needs to exist.
from pydantic import BaseModel
class Token(BaseModel):
    access_token: str
    token_type: str

router = APIRouter()

def create_access_token(data: dict, expires_delta: timedelta):
    from jose import jwt
    from datetime import datetime, timezone
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: IAuthService = Depends(get_auth_service)
):
    """OAuth2 compatible token login, get an access token for future requests."""
    user = auth_service.authenticate_user(email=form_data.username, password=form_data.password)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup", response_model=UserResponse)
def signup(
    user_in: UserCreate,
    user_service: IUserService = Depends(get_user_service)
):
    """Create new user without the need to be logged in."""
    return user_service.create_user(user_in)
