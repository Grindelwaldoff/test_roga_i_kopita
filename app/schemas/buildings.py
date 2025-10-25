from pydantic import BaseModel, ConfigDict


class BuildingBase(BaseModel):
    """Базовая схема для зднаий"""
    id: int
    address: str
    latitude: float
    longitude: float
    model_config = ConfigDict(from_attributes=True)


class BuildingList(BuildingBase):
    """Схема для списка зданий."""
    pass
