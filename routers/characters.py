from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserDB
from security import get_current_user, require_admin, require_moderator

import crud.characters
from deps import get_db
from schemas.characters import CreateCharacter,Character

router = APIRouter(
    prefix="/characters",
    tags=["Character"]
)

security = HTTPBearer()

@router.post("/create", response_model=Character)
async def create_character(
    character: CreateCharacter,
    current_user: UserDB = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    return await crud.characters.create_character(character, db)

@router.post("/{character_id}/assign/{user_id}")
async def assign_character_to_user(
    character_id: int = Path(..., gt=0),
    user_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    return await crud.characters.add_character_to_user(user_id, character_id, db)


@router.get("/", response_model=list[Character])
async def get_all_characters(db: AsyncSession = Depends(get_db)):
    return await crud.characters.get_characters(db)


@router.get("/{character_id}", response_model=Character)
async def get_character_by_id(character_id: int = Path(..., gt=0),db: AsyncSession = Depends(get_db)):
    result = await crud.characters.get_character_by_id(character_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    return result


@router.get("/user/{user_id}", response_model=list[Character])
async def get_characters_by_user(user_id: int = Path(..., gt=0),db: AsyncSession = Depends(get_db)):
    return await crud.characters.get_user_characters(user_id, db)


