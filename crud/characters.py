from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.suite.test_reflection import users

from models import CharacterDB, UserDB
from schemas.characters import CreateCharacter


async def create_character(character: CreateCharacter, db: AsyncSession):
    result = await db.execute(
        select(CharacterDB).where(CharacterDB.name == character.name)
    )
    existing_character = result.scalar_one_or_none()
    if existing_character is not None:
        raise HTTPException(
            status_code=400,
            detail="Персонаж с таким именем уже существует"
        )

    new_character = CharacterDB(
        name=character.name,
        base_damage=character.base_damage,
        base_health=character.base_health,
        base_speed=character.base_speed
    )

    db.add(new_character)
    await db.commit()
    await db.refresh(new_character)
    return new_character


async def add_character_to_user(
        user_id: int,
        character_id: int,
        db: AsyncSession
):
    result = await db.execute(
        select(UserDB).where(UserDB.user_id == user_id)
    )
    user = result.scalar_one_or_none()

    result = await db.execute(
        select(CharacterDB).where(CharacterDB.character_id == character_id)
    )
    character = result.scalar_one_or_none()

    if not user or not character:
        raise HTTPException(404, "Пользователь или персонаж не найден")

    if character in user.characters:
        raise HTTPException(400, "Пользователь уже имеет этого персонажа")

    user.characters.append(character)
    await db.commit()

    return {"message": f"Персонаж {character.name} добавлен пользователю {user.username}"}


async def get_characters(db: AsyncSession):
    result = await db.execute(select(CharacterDB))
    return result.scalars().all()


async def get_character_by_id(character_id: int, db: AsyncSession):
    result = await db.execute(
        select(CharacterDB).where(CharacterDB.character_id == character_id)
    )
    return result.scalar_one_or_none()


async def get_user_characters(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(UserDB).where(UserDB.user_id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(404, "Пользователь не найден")

    return user.characters


