from enum import Enum

class EquipmentCategory(str, Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    RING = "ring"

class BattleStatus(str, Enum):
    WAITING = "waiting"
    IN_PROCESS = "in_process"
    FINISHED = "finished"