
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession

import crud.users
import schemas.users
from deps import get_db
from schemas import users
from schemas.users import UserCreateRequest
from security import create_access_token

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

security = HTTPBearer()


@router.post("/create")
async def create_user(user: UserCreateRequest, db: AsyncSession = Depends(get_db)):
    result = await crud.users.create_user(user, db)
    return schemas.users.UserCreateResponse(
        success = True,
        message = "Пользователь успешно создан",
        username = result.username,
        email = result.email
    )


@router.post("/login", response_model=users.TokenResponse)
async def login(
        login_data: users.UserLoginRequest,
        db: AsyncSession = Depends(get_db)
):
    user = await crud.users.login_user(login_data, db)

    token_data = {"user_id": user.user_id, "username": user.username}
    access_token = create_access_token(token_data)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=users.UserResponse)
async def get_me(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
):
    user = await crud.users.get_me(credentials, db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user