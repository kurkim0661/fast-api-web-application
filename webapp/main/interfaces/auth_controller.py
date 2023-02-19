from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import status
from jose import jwt, JWTError

from webapp.main.buiseness.auth_service import AuthService
from webapp.main.containers import Container
from webapp.main.domain.dto.token import TokenData, Token
from webapp.main.domain.dto.user import UserDTO
from webapp.main.infra.persistence.user_repository import UserRepository

router = APIRouter()  # APIRouter()
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@inject
async def get_current_user(token: str = Depends(oauth2_scheme), users_repo: UserRepository = Depends(Provide[Container.users_repository])):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = users_repo.get_by_username(username)
    if user is None:
        raise credentials_exception

    user_dto = UserDTO(username=user.username, email=user.email, hashed_password=user.hashed_password, is_active=user.is_active)
    return user_dto


async def get_current_active_user(current_user: UserDTO = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    else:
        return current_user


@router.post("/token", response_model=Token)
@inject
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(Provide[Container.auth_service]), jwt_util=Depends(Provide[Container.jwt_util])):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_util.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/token/me")
async def read_users_me(current_user: UserDTO = Depends(get_current_active_user)) -> UserDTO:
    return current_user


@router.get("/users/me/items", response_model=None)
async def read_own_items(current_user: UserDTO = Depends(get_current_active_user)) -> list:
    return [{"item_id": "Foo", "owner": current_user.username}]
