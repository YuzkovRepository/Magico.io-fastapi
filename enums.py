from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class EquipmentCategory(str, Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    RING = "ring"

class BattleStatus(str, Enum):
    WAITING = "waiting"
    IN_PROCESS = "in_process"
    FINISHED = "finished"