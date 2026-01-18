from pydantic import BaseModel, Field, ConfigDict


class CreateCharacter(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    base_health: int = Field(ge=10,le=500)
    base_damage: int = Field(ge=10,le=500)
    base_speed: float = Field(ge=10.0,le=500.0)

class Character(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    base_health: int = Field(ge=10, le=500)
    base_damage: int = Field(ge=10, le=500)
    base_speed: float = Field(ge=10.0, le=500.0)

    model_config = ConfigDict(from_attributes=True)