from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserDB
from schemas import users
import security

async def create_user(user: users.UserCreateRequest, db: AsyncSession):
    result = await db.execute(select(func.count())
                              .where(UserDB.username == user.username))
    if result.scalar() > 0:
        raise HTTPException(status_code=400, detail="Пользователь с таким ником уже существует")
    result = await db.execute(select(func.count())
                              .where(UserDB.email == user.email))
    if result.scalar() > 0:
        raise HTTPException(status_code=400, detail="Пользователь с таким электронным адресом уже существует")

    new_user = UserDB(
        username=user.username,
        email=user.email,
        hashed_password=security.get_password_hash(user.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def login_user(login_data: users.UserLoginRequest, db: AsyncSession):
    result = await db.execute(
        select(UserDB).where(UserDB.email == login_data.email)
    )
    user = result.scalar_one_or_none()

    if not user or not security.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")

    return user

async def get_me(credentials: HTTPAuthorizationCredentials, db: AsyncSession):
    token = credentials.credentials
    payload = security.verify_token(token)

    result = await db.execute(
        select(UserDB).where(UserDB.user_id == payload["user_id"])
    )
    return result.scalar_one_or_none()
