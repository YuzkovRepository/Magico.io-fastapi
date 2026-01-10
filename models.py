from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, Boolean, func, ForeignKey, UniqueConstraint, \
    Table
from sqlalchemy.orm import relationship

from enums import EquipmentCategory, BattleStatus

from database import Base

user_characters = Table(
    'user_characters',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True),
    Column('character_id', Integer, ForeignKey('characters.character_id', ondelete='CASCADE'), primary_key=True),
    Column('level', Integer, default=1),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column('is_active', Boolean, default=False)
)

class UserDB(Base):
    __tablename__="users"
    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(30), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    coins = Column(Integer, default=0)
    crystals = Column(Integer, default=0)

    characters = relationship(
        "CharacterDB",
        secondary=user_characters,
        back_populates="users",
        lazy="selectin"
    )

    equipment_instances = relationship(
        "UserEquipmentDB",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    battle_participants = relationship(
        "BattleParticipantDB",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @property
    def total_health_bonus(self):
        return sum(
            eq.template.health_bonus
            for eq in self.equipment_instances
            if eq.is_equipped
        )

    @property
    def total_damage_bonus(self):
        return sum(
            eq.template.damage_bonus
            for eq in self.equipment_instances
            if eq.is_equipped
        )

    @property
    def total_speed_bonus(self):
        return sum(
            eq.template.speed_bonus
            for eq in self.equipment_instances
            if eq.is_equipped
        )

class CharacterDB(Base):
    __tablename__="characters"
    character_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable = False, unique=True)
    base_health = Column(Integer)
    base_damage = Column(Integer)
    base_speed = Column(Float, default=1)

    users = relationship(
        "UserDB",
        secondary=user_characters,
        back_populates="characters",
        lazy="selectin"
    )

class EquipmentDB(Base):
    __tablename__="equipments"
    equipment_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(50), unique=True)
    description = Column(String(255))
    equipment_category = Column(Enum(EquipmentCategory))

    health_bonus = Column(Integer, default=0)
    damage_bonus = Column(Integer, default=0)
    speed_bonus = Column(Float, default=0)

    user_instances = relationship(
        "UserEquipmentDB",
        back_populates="template",
        cascade="all, delete-orphan"
    )


class UserEquipmentDB(Base):
    __tablename__ = "user_equipment"

    user_equipment_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    equipment_id = Column(Integer, ForeignKey('equipments.equipment_id', ondelete='CASCADE'), nullable=False)

    # Индивидуальные свойства экземпляра
    level = Column(Integer, default=1)
    durability = Column(Integer, default=100)
    is_equipped = Column(Boolean, default=False)

    user = relationship("UserDB", back_populates="equipment_instances")
    template = relationship("EquipmentDB", back_populates="user_instances")


# class AbilityDB(Base):
#     __tablename__="abilities"
#     ability_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
#     name = Column(String(50), nullable=False)
#     level = Column(Integer, default=1)

class ArenaDB(Base):
    __tablename__ = "arenas"
    arena_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(20), nullable=False, unique=True)

    battles = relationship("BattleDB", back_populates="arena", cascade="all, delete-orphan")

class BattleDB(Base):
    __tablename__ = "battles"
    battle_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    arena_id = Column(Integer, ForeignKey("arenas.arena_id", ondelete="CASCADE"))
    status = Column(Enum(BattleStatus), default=BattleStatus.WAITING)
    max_players = Column(Integer, default=8)
    current_players = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)

    arena = relationship("ArenaDB", back_populates="battles")
    battle_participants = relationship("BattleParticipantDB", back_populates="battle", cascade="all, delete-orphan")

class BattleParticipantDB(Base):
    __tablename__ = "battle_participants"
    battle_participant_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    battle_id = Column(Integer, ForeignKey("battles.battle_id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    current_health = Column(Integer, default=100)
    current_mana = Column(Integer, default=0)
    position_x = Column(Float, default=0.0)
    position_y = Column(Float, default=0.0)
    kills = Column(Integer, default=0)

    is_alive = Column(Boolean, default=True)

    battle = relationship("BattleDB", back_populates="battle_participants")
    user = relationship("UserDB", back_populates="battle_participants")
    __table_args__ = (
        # Участник не может быть дважды в одной битве
        UniqueConstraint('battle_id', 'user_id', name='uq_battle_user'),
    )

